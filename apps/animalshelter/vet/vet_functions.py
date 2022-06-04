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

# Veterinarian

# Show Vet Table
@app.callback(
    [
        Output('vet_table', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('adminshelter_data', 'data'),
        Input('vet_search', 'value')
    ]
)
def vettable(pathname, shelterdata, searchval):
    if pathname == '/vet/menu':

        shelter_data_df = pd.DataFrame.from_records(shelterdata)

        # Obtain records from SQL
        sql = """
        SELECT vet_n, vet_m, vet_a, vet_no, vet_s, vet_l, vet_sal, vet_spec
        FROM veterinarian
        WHERE vet_del_ind = FALSE
        AND shelter_n = %s
        """

        values = [int(shelter_data_df.at[0, 'SHELTER ID'])]

        if searchval:
            sql += "\nAND vet_m ILIKE %s"
            values.append(f"%{searchval}%")

        cols = ['VET #', 'Name', 'Age', 'Number', 'Sex', 'Address', 'Salary', 'Specialization']

        vet_df = db.querydatafromdatabase(sql, values, cols)

        if vet_df.shape[0]:
            vet_df = vet_df[['VET #', 'Name', 'Age', 'Number', 'Sex', 'Address', 'Salary', 'Specialization']]

            linkcolumn = {} # Adjust button placement (front-end problem)
            for index, row in vet_df.iterrows():
                linkcolumn[index] = html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                dbc.Button(
                                    'Edit',
                                    href='/vet/info?mode=edit&vetid='+str(row['VET #']),
                                    n_clicks = 0
                                ),
                                width = 1),

                                dbc.Col(
                                    dbc.Button(
                                        'Delete',
                                        href = '/vet/menu?mode=delete&vetid='+str(row['VET #']),
                                        id = {
                                            'type': 'del_vet',
                                            'index': str(row['VET #'])
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

            data_dict = vet_df.to_dict()
            data_dict.update(dictionarydata)

            vet_df = pd.DataFrame.from_dict(data_dict)

            vet_df = vet_df[['VET #', 'Name', 'Age', 'Number', 'Sex', 'Address', 'Salary', 'Specialization', 'Action']]

            vet_df.sort_values(by='VET #', inplace = True)
            vet_df.drop(columns=['VET #'], inplace=True)

        table = dbc.Table.from_dataframe(vet_df, striped=True, bordered=True,
                        hover=True, size='sm',
                        style = {
                            'whiteSpace': 'normal',
                            'height': 'auto'
                        })

        if vet_df.shape[0]:
            return [table]
        else:
            return ['No records to display']
    else:
        raise PreventUpdate

# Submit Vet Record
@app.callback(
    [
        Output('vet_addalert', 'color'),
        Output('vet_addalert', 'children'),
        Output('vet_addalert', 'is_open'),
        Output('vet_addsuccessmodal', 'is_open')
    ],
    [
        Input('adminshelter_data', 'data'),
        Input('sub_vet', 'n_clicks'),
        Input('vet_close_button', 'n_clicks')
    ],
    [
        State('vet_name', 'value'),
        State('vet_age', 'value'),
        State('vet_l', 'value'),
        State('vet_no', 'value'),
        State('vet_s', 'value'),
        State('vet_spec', 'value'),
        State('vet_sal', 'value'),
        State('url', 'search')
    ]
)
def vet_addrecord(shelterdata, submitbtn, closebtn, vetname, vetage, vetloc, vetno, vetsex, vetspec, vetsal, search):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'sub_vet' and submitbtn:

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            sql = """
            SELECT vet_n FROM veterinarian
            """

            values = []

            cols = ['ID #']

            df = db.querydatafromdatabase(sql, values, cols)

            shelter_data_df = pd.DataFrame.from_records(shelterdata)

            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query)['mode'][0]

            if create_mode == 'add':

                vet_id = 1
                shelter_id = int(shelter_data_df.at[0, 'SHELTER ID'])

                if len(df) == 0:
                    vet_id = 1
                else:
                    vet_id = len(df) + 1

                sql_add = """
                INSERT INTO veterinarian(vet_n, vet_m, vet_a, vet_s, vet_l, vet_no, 
                vet_spec, vet_sal, vet_del_ind, shelter_n)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values_add = [vet_id, vetname, vetage, vetsex, vetloc, 
                vetno, vetspec, vetsal, False, shelter_id]

                db.modifydatabase(sql_add, values_add)

                modal_open = True

                return [alert_color, alert_text, alert_open, modal_open]
            
            elif create_mode == 'edit':

                # Obtain vet id
                vet_id = int(parse_qs(parsed.query)['vetid'][0])
                shelter_id = int(shelter_data_df.at[0, 'SHELTER ID'])

                # Generate SQL script
                sql = """
                UPDATE veterinarian
                SET
                    vet_m = %s,
                    vet_a = %s,
                    vet_s = %s,
                    vet_l = %s,
                    vet_no = %s,
                    vet_spec = %s,
                    vet_sal = %s
                WHERE
                vet_n = %s AND
                shelter_n = %s"""

                values = [vetname, vetage, vetsex, vetloc, vetno, vetspec, vetsal, vet_id, shelter_id]

                db.modifydatabase(sql, values)

                modal_open = True

                return [alert_color, alert_text, alert_open, modal_open]

            else:
                raise PreventUpdate

        elif event_id == 'vet_close_button' and closebtn:

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            return [alert_color, alert_text, alert_open, modal_open]
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# Edit Veterinarian – Change Data Store
@app.callback(
    [
        Output('vet_add_store', 'data')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def edit_medicine_entry_dsv(pathname, search):
    if pathname == '/vet/info':
        
        parsed = urlparse(search)

        create_mode = parse_qs(parsed.query)['mode'][0]

        vet_data_status = 1 if create_mode == 'edit' else 0

        return [vet_data_status]
    
    else:
        raise PreventUpdate

# Edit Function – Pet
@app.callback(
    [
        Output('vet_name', 'value'),
        Output('vet_age', 'value'),
        Output('vet_l', 'value'),
        Output('vet_no', 'value'),
        Output('vet_s', 'value'),
        Output('vet_spec', 'value'),
        Output('vet_sal', 'value')
    ],
    [
        Input('vet_add_store', 'modified_timestamp')
    ],
    [
        State('vet_add_store', 'data'),
        State('url', 'search'),
        State('adminshelter_data', 'data')
    ]
)
def edit_pet_entry_reflect(timestamp, data, search, shelterdata):
    if data:

        # Get Vet ID
        parsed = urlparse(search)
        vet_id = int(parse_qs(parsed.query)['vetid'][0])
        shelter_id = int(shelterdata[0]['SHELTER ID'])

        # Query from DB
        sql = """
            SELECT vet_m, vet_a, vet_l, vet_no, vet_s, vet_spec, vet_sal FROM veterinarian
            WHERE vet_n = %s AND shelter_n = %s
        """
        
        values = [vet_id, shelter_id]

        cols = ['vet_m', 'vet_a', 'vet_l', 'vet_no', 'vet_s', 'vet_spec', 'vet_sal']

        df = db.querydatafromdatabase(sql, values, cols)

        vet_name = df['vet_m'][0]
        vet_age = df['vet_a'][0]
        vet_add = df['vet_l'][0]
        vet_no = df['vet_no'][0]
        vet_sex = df['vet_s'][0]
        vet_spec = df['vet_spec'][0]
        vet_sal = df['vet_sal'][0]

        return [vet_name, vet_age, vet_add, vet_no, vet_sex, vet_spec, vet_sal]

    else:
        raise PreventUpdate
    
# Delete Veterinarian
@app.callback(
    [
        Output('del_vet_modal', 'is_open')
    ],
    [
        Input({'type': 'del_vet', 'index': ALL}, 'n_clicks'),
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)
def delete_vet(selectedvet, pathname, search):
    if pathname == '/vet/menu':
        ctx = dash.callback_context
        if ctx.triggered:
            event = ctx.triggered[0]['prop_id'].split('.')[0]
            event = json.loads(event)

            eventid = event['type']

            if eventid == 'del_vet' and selectedvet:
                parsed = urlparse(search)

                if not parsed.query:
                    raise PreventUpdate

                elif parsed.query:
                    mode = parse_qs(parsed.query)['mode'][0]

                    if not mode:
                        raise PreventUpdate
                    
                    elif mode == 'delete':

                        vet_id = parse_qs(parsed.query)['vetid'][0]

                        sql = """
                        UPDATE veterinarian
                        SET vet_del_ind = True
                        WHERE vet_n = %s
                        """

                        values = [vet_id]

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