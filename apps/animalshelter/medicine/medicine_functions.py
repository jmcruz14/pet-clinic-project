from re import S
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

from dash.dependencies import Input, Output, State, MATCH, ALL, ALLSMALLER
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import json


from app import app
import apps.commonmodules as cm
import apps.dbconnect as db

#  Show Amount
@app.callback(
    [
        Output('med_cn', 'children')
    ],
    [
        Input('med_cn_slider', 'value')
    ]
)
def update_slider_amount(number):
    if number >= 0:
        return ['{}'.format(number)]
    else:
        return ['Invalid value. Please try again!']

# Compute for Total Cost
@app.callback(
    [
        Output('med_tc', 'children')
    ],
    [
        Input('med_c', 'value'),
        Input('med_cn_slider', 'value')
    ]
)
def med_calculator(cost, count):
    if cost and count:
        total_cost = float(cost) * float(count)
        total_cost = format(round(float(total_cost), 2), '.2f')

        return [total_cost]
    elif cost == 0 or count == 0:
        total_cost = format(0, '.2f')

        return [total_cost]
    else:
        raise PreventUpdate

# Submit Medicine Details
@app.callback(
    [
        Output('med_addalert', 'color'),
        Output('med_addalert', 'children'),
        Output('med_addalert', 'is_open'),
        Output('med_addsuccessmodal', 'is_open')
    ],
    [
        Input('adminshelter_data', 'data'),
        Input('sub_md', 'n_clicks'),
        Input('continue_medaddrecord', 'n_clicks')
    ],
    [
        State('med_name', 'value'),
        State('med_cn_slider', 'value'),
        State('med_type', 'value'),
        State('med_c', 'value'),
        State('med_tc', 'children'),
        State('url', 'search')
    ]
)
def submit_medicineentry(shelterdata, submitbtn, closebtn, medm, medcn, medtype, medc, medtc, search):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'sub_md' and submitbtn:

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # Required entries
            if not medm:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the name of the medicine.'
            elif not medcn:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the number of available medicine.'
            elif not medtype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the type of medicine'
            elif not medc:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the cost per medicine.'
            else:

            # Mode condition
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':

                    # Check dataframe length
                    sql_check = """
                    SELECT m.med_n, m.med_m, m.med_type, m.med_cn, m.med_c, m.med_tc FROM medicine m
                    """
                    values_check = []

                    cols = [
                        'MED ID', 'NAME', 'TYPE', 'COUNT', 'COST', 
                        'TOTAL COST']

                    df = db.querydatafromdatabase(sql_check, values_check, cols)

                    med_id = 1

                    if len(df) == 0:
                        med_id = 1
                    elif len(df) != 0:
                        med_id = len(df) + 1

                    shelter_data_df = pd.DataFrame.from_records(shelterdata)                

                    shelter_id = int(shelter_data_df.at[0, 'SHELTER ID'])

                    med_date_entr = datetime.now().strftime("%Y-%m-%d")
                    
                    sql_add = """
                    INSERT INTO medicine(med_n, shelter_n, med_m, med_type, med_cn, med_c, med_tc, med_date_entr, med_del_ind)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values_add = [
                        med_id, shelter_id, medm, medtype, medcn, medc, 
                        medtc, med_date_entr, False]

                    db.modifydatabase(sql_add, values_add)

                    modal_open = True

                    return [alert_color, alert_text, alert_open, modal_open]
                
                elif create_mode == 'edit':
                    
                    # Obtain med id
                    med_id = int(parse_qs(parsed.query)['medid'][0])

                    # Generate SQL script

                    sql = """
                    UPDATE medicine
                    SET
                        med_m = %s,
                        med_type = %s,
                        med_c = %s,
                        med_cn = %s,
                        med_tc = %s
                    WHERE
                        med_n = %s"""

                    values = [medm, medtype, medc, medcn, medtc, med_id]

                    db.modifydatabase(sql, values)

                    modal_open = True

                    return [alert_color, alert_text, alert_open, modal_open]

        elif eventid == 'continue_medaddrecord' and closebtn:
            modal_open = False
            alert_color = ''
            alert_text = ''
            alert_open = False
            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

# Show Medicine Table
@app.callback(
    [
        Output('med_table', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('adminshelter_data', 'data')
        #Input('med_search', 'value') # search_value parameter nito
    ]
)
def med_list_filter(pathname, shelterdata):
    if pathname == '/medicine':

        # Obtain records from SQL
        sql = """
        SELECT m.med_n as ID, m.med_m as NAME, m.med_type as TYPE, m.med_cn as COUNT, m.med_c as COST, m.med_tc as TOTAL_COST
        FROM medicine m
        WHERE med_del_ind = FALSE
        AND shelter_n = %s
        """

        shelter_data_df = pd.DataFrame.from_records(shelterdata)

        values = [int(shelter_data_df.at[0, 'SHELTER ID'])]

        cols = ['ID #', 'Name', 'Med Type', 'In Stock', 'Unit Cost', 'Total Cost']

        df = db.querydatafromdatabase(sql, values, cols)

        #2. Create the html element to return to the Div

        if df.shape[0]: #if rows in the dataframe > 0

            linkcolumn = {} # Adjust button placement (front-end problem)
            for index, row in df.iterrows():
                linkcolumn[index] = html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                dbc.Button(
                                    'Edit',
                                    href='/medicine/medinfo?mode=edit&medid='+str(row['ID #']),
                                    n_clicks = 0
                                ),
                                width = 1),

                                dbc.Col(
                                    dbc.Button(
                                        'Delete',
                                        href = '/medicine?mode=delete&medid='+str(row['ID #']),
                                        id = {
                                            'type': 'del_medicine',
                                            'index': str(row['ID #'])
                                            },
                                        n_clicks = 0
                                    ),
                                    width = {'size': 1, 'offset': 2}
                                )
                            ],

                            justify='evenly'
                        )
                    ]
                )
            
            # Name the column of hyperlinks - Action
            dictionarydata = {'Action': linkcolumn}

            data_dict = df.to_dict()
            data_dict.update(dictionarydata)

            df = pd.DataFrame.from_dict(data_dict)

            df = df[['ID #', 'Name', 'Med Type', 'In Stock', 'Unit Cost', 'Total Cost', 'Action']]

            df.sort_values(by='ID #', inplace = True)
            df.drop(columns=['ID #'], inplace = True)

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                        hover=True, size='sm')

        if df.shape[0]:
            return [table]
        else:
            return ['No records to display.']

    else:
        raise PreventUpdate

# Edit Medicine – Update Data Store Variable
@app.callback(
    [
        Output('med_data_store', 'data')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def edit_medicine_entry_dsv(pathname, search):
    if pathname == '/medicine/medinfo':
        
        parsed = urlparse(search)

        create_mode = parse_qs(parsed.query)['mode'][0]

        med_data = 1 if create_mode == 'edit' else 0

        return [med_data]
    
    else:
        raise PreventUpdate

# Edit Function – Medicine
@app.callback(
    [
        Output('med_name', 'value'),
        Output('med_type', 'value'),
        Output('med_cn_slider', 'value'),
        Output('med_c', 'value')
    ],
    [
        Input('med_data_store', 'modified_timestamp')
    ],
    [
        State('med_data_store', 'data'),
        State('url', 'search')
    ]
)
def edit_med_entry_reflect(timestamp, data, search):
    print('med data status:', data)
    if data:

        # Get Med ID
        parsed = urlparse(search)
        med_id = int(parse_qs(parsed.query)['medid'][0])
        
        # Query from DB
        sql = """
            SELECT med_m, med_type, med_cn, med_c FROM medicine
            WHERE med_n = %s
        """
        
        values = [med_id]

        cols = ['med_n', 'med_type', 'med_count', 'med_ucost']

        df = db.querydatafromdatabase(sql, values, cols)

        med_name = df['med_n'][0]
        med_type = df['med_type'][0]
        med_count = df['med_count'][0]
        med_unitcost = df['med_ucost'][0]

        return [med_name, med_type, med_count, med_unitcost]

    else:
        raise PreventUpdate

# Delete Function – Medicine
@app.callback(
    [
        Output('delmed_success_modal', 'is_open'),
    ],
    [
        Input({'type': 'del_medicine', 'index': ALL}, 'n_clicks'),
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def delete_med(selectedmedicine, pathname, search):
    if pathname == '/medicine':
        ctx = dash.callback_context
        if ctx.triggered:

            event = ctx.triggered[0]['prop_id'].split('.')[0]
            event = json.loads(event)

            eventid = event['type']

            if eventid == 'del_medicine' and selectedmedicine:
                parsed = urlparse(search)

                if not parsed.query:
                    raise PreventUpdate

                elif parsed.query:
                    mode = parse_qs(parsed.query)['mode'][0]

                    if not mode:
                        raise PreventUpdate
                    
                    elif mode == 'delete':

                        med_id = parse_qs(parsed.query)['medid'][0]

                        sql = """
                        UPDATE medicine
                        SET med_del_ind = True
                        WHERE med_n = %s
                        """

                        values = [med_id]

                        db.modifydatabase(sql, values)

                        return [True]
                    
                    else:
                        raise PreventUpdate
                    
                else:
                    raise PreventUpdate
            
            else:
                raise PreventUpdate

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate
    