
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

# Record Pet Entry
# Completion progress: no edit entry / bug fix for multiple entries
@app.callback(
    [
        Output('pet_addalert', 'color'),
        Output('pet_addalert', 'children'),
        Output('pet_addalert', 'is_open'),
        Output('pet_addsuccessmodal', 'is_open')
    ],
    [
        Input('sub_pd', 'n_clicks'),
        Input('continue_petaddrecord', 'n_clicks')
    ],
    [
        State('pet_rd', 'date'),
        State('pet_name', 'value'),
        State('pet_breed', 'value'),
        State('pet_sex', 'value'),
        State('pet_age', 'value'),
        State('pet_adpt_stat_box', 'checked'),
        State('pet_story', 'value'),
        State('pet_mr', 'value'),
        State('adminshelter_data', 'data'),
        State('url', 'search')
    ]
)
def pet_add(submitbtn, closebtn, prdate, pname, pbreed, psex, page, petadptstat, pstory, precords, shelterdata, search):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'sub_pd' and submitbtn:
        
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # Required entries
            if not prdate:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the date of rescue.'
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            elif not pstory:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the pet story.'
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            elif not pname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the pet name.'
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            elif not pbreed:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the pet breed.'
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            elif not psex:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the pet sex.'
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            elif not page:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the pet age.'
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            elif not pstory:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Please provide the rescue story.'
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            if not precords:
                no_update = dash.no_update

            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query)['mode'][0]

            if create_mode == 'add':

                # Check dataframe length
                sql_check = """
                SELECT pet_n, pet_m, pet_b, pet_s, pet_rs, pet_rd, pet_a, pet_mr, pet_delete_ind FROM pet
                """
                values_check = []

                cols = [
                    'PET ID', 'NAME', 'BREED', 'SEX', 'RESCUE STORY', 
                    'RESCUE DATE', 'AGE', 'MEDICAL RECORDS', 'DELETED?']

                df = db.querydatafromdatabase(sql_check, values_check, cols)

                pet_id = 1

                if len(df) == 0:
                    pet_id = 1
                elif len(df) != 0:
                    pet_id = len(df) + 1
                
                shelter_data_df = pd.DataFrame.from_records(shelterdata)

                shelter_id = int(shelter_data_df.at[0, 'SHELTER ID'])

                pet_date_entr = datetime.now().strftime("%Y-%m-%d")

                sql_add = """
                INSERT INTO pet(PET_N, SHELTER_N, PET_M, PET_B, PET_S, PET_RS, PET_RD, PET_A,
                PET_MR, PET_DATE_ENTR, PET_ADPT_STAT, PET_DELETE_IND)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values_add = [
                    pet_id, shelter_id, pname, pbreed, psex, pstory, 
                    prdate, page, precords, pet_date_entr, petadptstat, False]

                db.modifydatabase(sql_add, values_add)

                return [dash.no_update, dash.no_update, dash.no_update, True]

            elif create_mode == 'edit':

                # Obtain pet id
                pet_id = int(parse_qs(parsed.query)['petid'][0])

                shelter_data_df = pd.DataFrame.from_records(shelterdata)

                shelter_id = int(shelter_data_df.at[0, 'SHELTER ID'])

                # Generate SQL script
                sql = """
                UPDATE pet
                SET
                    pet_m = %s,
                    pet_b = %s,
                    pet_s = %s,
                    pet_rs = %s,
                    pet_rd = %s,
                    pet_a = %s,
                    pet_mr = %s,
                    pet_adpt_stat = %s
                WHERE
                pet_n = %s AND
                shelter_n = %s"""

                values = [pname, pbreed, psex, pstory, prdate, page, precords, petadptstat, pet_id, shelter_id]

                db.modifydatabase(sql, values)

                modal_open = True

                return [alert_color, alert_text, alert_open, modal_open]

            else:
                raise PreventUpdate
            
        elif eventid == 'continue_petaddrecord' and closebtn:
            modal_open = False
            alert_color = ''
            alert_text = ''
            alert_open = False
            return [alert_color, alert_text, alert_open, modal_open]
        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

# Show Pet Table
# Assignment: Fix Pet Table Delete Function
@app.callback(
    [
        Output('pet_table', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('adminshelter_data', 'data'),
        Input('pet_search', 'value')
    ]
)
def pettable(pathname, shelterdata, searchval):
    if pathname == '/pet/menu':

        shelter_data_df = pd.DataFrame.from_records(shelterdata)

        # Obtain records from SQL
        sql = """
        SELECT pet_n, pet_m, pet_b, pet_a, pet_s, pet_rd, pet_adpt_stat
        FROM pet 
        WHERE pet_delete_ind = FALSE
        AND shelter_n = %s
        AND NOT EXISTS (SELECT 1
                        FROM adoption
                        WHERE adoption.pet_n = pet.pet_n
                        AND adopt_order_r ILIKE 'P' AND 'Y')
        """

        values = [int(shelter_data_df.at[0, 'SHELTER ID'])]

        if searchval:
            sql += "\nAND pet_m ILIKE %s"
            values.append(f"%{searchval}%")

        cols = ['ID #', 'Name', 'Breed', 'Age', 'Sex', 'Date of Rescue', 'Ready for Adoption']

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]: # Convert adoption status checklist into a statement (convert the df values)
            
            df['Ready for Adoption'] = df['Ready for Adoption'].apply(lambda x: "Yes" if x else "No")

            # Creating the hyperlinks – Edit / Delete
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        'Edit',
                                        href='/pet/add?mode=edit&petid='+str(row['ID #']),
                                        id = {
                                        'type': 'edit_pet_entry',
                                        'index': str(row['ID #'])
                                        }
                                    ),

                                    width=1
                                ),

                                dbc.Col(
                                    dbc.Button(
                                        'Delete',
                                        href='/pet/menu?mode=delete&petid='+str(row['ID #']),
                                        id = {
                                            'type': 'delete_pet',
                                            'index': str(row['ID #'])
                                        }
                                    ),

                                    width={'size': 2, 'offset': 2}
                                )
                            ]
                        )
                    ]
                )
            
            # Name the column of hyperlinks - Action
            dictionarydata_action = {'Action': linkcolumn}

            data_dict = df.to_dict()
            data_dict.update(dictionarydata_action)

            df = pd.DataFrame.from_dict(data_dict)

            df = df[['ID #', 'Name', 'Breed', 'Age', 'Sex', 'Date of Rescue', 'Ready for Adoption', 'Action']]

            df.sort_values(by='ID #', inplace = True)
            df.drop(columns=['ID #'], inplace = True)

        table = dbc.Table.from_dataframe(
                df, 
                striped=True, 
                bordered=True,
                hover=True,
                size='sm',
                style = {
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                id = 'pet_table_data')
        
        if df.shape[0]:
            return [table]
        else:
            return ['No records to display.']
        
    else:
        raise PreventUpdate

# Edit Pet – Update Data Store Variable
@app.callback(
    [
        Output('pet_data_store', 'data'),
        Output('pet_adpt_stat_div', 'hidden')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def edit_medicine_entry_dsv(pathname, search):
    if pathname == '/pet/add':
        
        parsed = urlparse(search)

        create_mode = parse_qs(parsed.query)['mode'][0]

        pet_data_status = 1 if create_mode == 'edit' else 0

        if create_mode == 'edit':
            pet_data_status = 1
            hidden_div = False

            return [pet_data_status, hidden_div]

        else:
            pet_data_status = 0
            hidden_div = True

            return [pet_data_status, hidden_div]
    
    else:
        raise PreventUpdate

# Edit Function – Pet
@app.callback(
    [
        Output('pet_rd', 'date'),
        Output('pet_name', 'value'),
        Output('pet_breed', 'value'),
        Output('pet_sex', 'value'),
        Output('pet_age', 'value'),
        Output('pet_story', 'value'),
        Output('pet_mr', 'value'),
        Output('pet_adpt_stat_box', 'checked')
    ],
    [
        Input('pet_data_store', 'modified_timestamp')
    ],
    [
        State('pet_data_store', 'data'),
        State('url', 'search'),
        State('adminshelter_data', 'data')
    ]
)
def edit_pet_entry_reflect(timestamp, data, search, shelterdata):
    if data:

        # Get Pet ID
        parsed = urlparse(search)
        pet_id = int(parse_qs(parsed.query)['petid'][0])
        shelter_id = int(shelterdata[0]['SHELTER ID'])

        print(pet_id, shelter_id)
        
        # Query from DB
        sql = """
            SELECT pet_m, pet_b, pet_s, pet_rs, pet_rd, pet_a, pet_mr, pet_adpt_stat FROM pet
            WHERE pet_n = %s AND shelter_n = %s
        """
        
        values = [pet_id, shelter_id]

        cols = ['pet_name', 'pet_breed', 'pet_sex', 'pet_rs', 'pet_rd', 'pet_a', 'pet_mr', 'pet_adpt_stat']

        df = db.querydatafromdatabase(sql, values, cols)

        pet_name = df['pet_name'][0]
        pet_breed = df['pet_breed'][0]
        pet_sex = df['pet_sex'][0]
        pet_rstory = df['pet_rs'][0]
        pet_rdate = df['pet_rd'][0]
        pet_age = df['pet_a'][0]
        pet_mr = df['pet_mr'][0]
        pet_adpt_stat = df['pet_adpt_stat'][0]

        return [pet_rdate, pet_name, pet_breed, pet_sex, pet_age, pet_rstory, pet_mr, pet_adpt_stat]

    else:
        raise PreventUpdate

# Delete Function – Pet
@app.callback(
    [
        Output('delpet_success_modal', 'is_open'),
    ],
    [
        Input({'type': 'delete_pet', 'index': ALL}, 'n_clicks'),
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def delete_med(selectedmedicine, pathname, search):
    if pathname == '/pet/menu':
        ctx = dash.callback_context
        if ctx.triggered:

            event = ctx.triggered[0]['prop_id'].split('.')[0]
            event = json.loads(event)

            eventid = event['type']

            if eventid == 'delete_pet' and selectedmedicine:
                parsed = urlparse(search)

                if not parsed.query:
                    raise PreventUpdate

                elif parsed.query:
                    mode = parse_qs(parsed.query)['mode'][0]

                    if not mode:
                        raise PreventUpdate
                    
                    elif mode == 'delete':

                        pet_id = parse_qs(parsed.query)['petid'][0]

                        sql = """
                        UPDATE pet
                        SET pet_delete_ind = True
                        WHERE pet_n = %s
                        """

                        values = [pet_id]

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