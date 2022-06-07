#%%index
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

import webbrowser

import time

from app import app
import apps.commonmodules as cm
import apps.dbconnect as db
from apps import login_page
from apps.animalshelter import animalshelter_portal
from apps.animalshelter.pet import animalshelter_petadd
from apps.animalshelter.pet import animalshelter_petmenu
from apps.animalshelter.pet import pet_functions
from apps.animalshelter.vet import animalshelter_vet
from apps.animalshelter.vet import animalshelter_vetadd
from apps.animalshelter.vet import vet_functions
from apps.animalshelter.medicine import animalshelter_medicine
from apps.animalshelter.medicine import animalshelter_medicineadd
from apps.animalshelter.medicine import medicine_functions
from apps.animalshelter.events import animalshelter_animalcareevent
from apps.animalshelter import animalshelter_schedule
from apps.animalshelter import animalshelter_functions
from apps.animalshelter.events import animalshelter_adoptevent
from apps.animalshelter.adopter import animalshelter_addadopter
from apps.animalshelter.adopter import animalshelter_adopterlist
from apps.animalshelter.adopter import animalshelter_adoptionhistory
from apps.animalshelter.reports_folder import reports_page

# Standalone Functions
def grab_pet_status(row_id):

    # SQL Query
    sql = """
    SELECT pet_n, pet_adpt_stat from pet
    WHERE pet_delete_ind = False
    """

    values = [row_id]

    cols = ['ID #', 'Adopt Status']

    df = db.querydatafromdatabase(sql, values, cols)

    if df.at[0, 'Adopt Status'] == True:
        return df.at[0, 'Adopt Status']
    else:
        return False

## General Page Layout
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        dcc.Store(id='adminshelter_data', storage_type='session'),
        #dcc.Store(id='adopter_data', storage_type='session'),
        dcc.Store(id='vet_data', storage_type='session'),
        dcc.Store(id='pet_data', storage_type='session'),
        html.Div(id='navbar_type'),
        html.Div(id='page_content'),
    ]
)

#%% 

# Log-in and other global functions

## Log-in page
@app.callback(
    [
        Output('page_result', 'children'),
        Output('url', 'pathname'),
        Output('adminshelter_data', 'data'),
        Output('pet_data', 'data'),
        Output('vet_data', 'data')
    ],
    [
        Input('login', 'n_clicks'),
    ],
    [
        State('user', 'value'), 
        State('passw', 'value')
    ]
)
def login_account(n_clicks, uname, passw): #Work on this later # add href='/portal'
    ctx = dash.callback_context #<dash._callback_context.CallbackContext object at 0x117fc1550>
    if ctx.triggered: #[{'prop_id': 'login.n_clicks', 'value': 1}]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'login' and n_clicks:

            # Check for log-in details
            if not uname:
                response = html.Center("Please enter your username!", {'fontFamily': 'Avenir'})

                return [response, dash.no_update, dash.no_update, dash.no_update, dash.no_update]
            
            if not passw:
                response = html.Center("Please enter your password!", {'fontFamily': 'Avenir'})

                return [response, dash.no_update, dash.no_update, dash.no_update, dash.no_update]

            # Obtain SQL Records

            sql_shelter = """
            SELECT a.admin_n as adminid, a.admin_m as username, a.admin_pass as password, a.shelter_n as id, s.shelter_br as branch, s.shelter_l as address
            FROM administrator a INNER JOIN shelter s 
            ON a.shelter_n = s.shelter_n
            WHERE admin_del_ind = FALSE
            """
            values_shelter = []

            if uname and passw:
                sql_shelter += """
                AND ADMIN_M ILIKE %s
                AND ADMIN_PASS ILIKE %s
                """

                values_shelter = [uname, passw]
            
            cols_shelter = ['ADMIN ID','USERNAME', 'PASSWORD', 'SHELTER ID', 'BRANCH', 'ADDRESS']

            df_shelter = db.querydatafromdatabase(sql_shelter, values_shelter, cols_shelter)
            # [ADMIN ID USERNAME PASSWORD SHELTER ID BRANCH ADDRESS]

            if df_shelter.shape[0]:
                response = html.Center("Successful Login!", {'fontFamily': 'Avenir'})
                redirect = '/portal'

                sql_pet = """
                SELECT pet_n, pet_m, pet_b, pet_s, pet_rd, pet_adpt_stat, shelter_n FROM pet
                WHERE pet_delete_ind = FALSE
                AND shelter_n = %s
                """

                values_pet = [int(df_shelter.at[0, 'SHELTER ID'])]

                cols_pet = [
                    'ID #', 'Name', 'Breed', 
                    'Sex', 'Rescue Date', 
                    'Ready for Adoption?','Shelter #'
                    ]

                df_pet = db.querydatafromdatabase(sql_pet, values_pet, cols_pet)
                # [ID # Name Breed Sex Rescue Date Ready for Adoption? Shelter #]

                sql_vet = """
                SELECT vet_n, vet_m, vet_a, vet_no, vet_s, vet_l, vet_sal, vet_spec
                FROM veterinarian
                WHERE vet_del_ind = False
                AND shelter_n = %s"""

                values_vet = [int(df_shelter.at[0, 'SHELTER ID'])]

                cols_vet = ['VET #', 'Name', 'Age', 'Number', 'Sex', 'Address', 'Salary', 'Specialization']
                # [VET # Name Age Number Sex Address Salary Specialization]

                df_vet = db.querydatafromdatabase(sql_vet, values_vet, cols_vet)

                login_details = df_shelter.to_dict('records')

                # [{'ADMIN ID': 1, 'USERNAME': 'admin1', 'PASSWORD': 'password', 
                # 'SHELTER ID': 1, 'BRANCH': 'Nasugbu Shelter', 'ADDRESS': 'JP Laurel Street, 
                # Brgy. Lumbangan, Nasugbu, Batangas'}]

                pet_details = df_pet.to_dict('records')

                vet_details = df_vet.to_dict('records')
                
                return [response, redirect, login_details, pet_details, vet_details]

            # Click to send user to next page if successful
            # If log-in details are wrong, return incorrect entry

            else:
                response = html.Center("Incorrect Log-in Details, please try again!",
                style = {'fontFamily': 'Avenir'})

                failure = '/home'
                login_fail = ''
                pet_fail = ''
                vet_fail = ''

                return [response, failure, login_fail, pet_fail, vet_fail]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

#Display Page
@app.callback(
    [
        Output('navbar_type', 'children'),
        Output('page_content', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def displaypage(pathname):
    ctx = dash.callback_context
    returnlayout = []
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url': #add more urls here if we have one
            if pathname == '/' or pathname == '/home':
                returnlayout = login_page.login
                navbar = cm.navbar
                return [navbar, returnlayout]
            elif pathname == '/portal': #Make Portal page
                returnlayout = animalshelter_portal.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/pet/menu':
                returnlayout = animalshelter_petmenu.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/pet/add':
                returnlayout = animalshelter_petadd.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/medicine':
                returnlayout = animalshelter_medicine.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/medicine/medinfo':
                returnlayout = animalshelter_medicineadd.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/vet/menu':
                returnlayout = animalshelter_vet.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/vet/info':
                returnlayout = animalshelter_vetadd.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/adoptions':
                returnlayout = animalshelter_addadopter.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/adoptions/adopter_list':
                returnlayout = animalshelter_adopterlist.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/adoptions/history':
                returnlayout = animalshelter_adoptionhistory.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/reports':
                returnlayout = reports_page.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/schedule/adopt' or pathname == '/schedule/adopt?mode=select':
                returnlayout = animalshelter_adoptevent.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/schedule/animalcare_event':
                returnlayout = animalshelter_animalcareevent.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            elif pathname == '/schedule':
                returnlayout = animalshelter_schedule.layout
                navbar = cm.navbar_main
                return [navbar, returnlayout]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# Change Navbar Text according to log-in data
@app.callback(
    [
        Output('shelter_br', 'children'),
        Output('shelter_l', 'children')
    ],
    [
        Input('adminshelter_data', 'data')
    ]
)
def portal_details(logindata):
    if logindata:
        login_details = pd.DataFrame(logindata)

        return [login_details['BRANCH'], login_details['ADDRESS']]
    else: # no data entries in logindata – prevent bypassing
        raise PreventUpdate

#%%

# Adopter-related (Add an Adopter) Functions

# Show modal window of existing adopters
@app.callback(
    [
        Output('existing_adopter_modal', 'is_open'),
    ],
    [
        Input('adopter_exists', 'n_clicks')
    ]
)
def existingadopterwindow(existingbtn):
    ctx = dash.callback_context
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'adopter_exists' and existingbtn:
            open_state = True

            return [open_state]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# Show list of existing adopters in window
@app.callback(
    [
        Output('existing_adopter_list', 'children')
    ],
    [
        Input('existing_adopter_modal', 'is_open')
    ]
)
def existingadopterlist(open_status):
    if open_status == True:

        # Get SQL
        sql = """
        SELECT adopter_n, adopter_m, adopter_a, adopter_s, 
        adopter_no, adopter_l, adopter_occ 
        FROM adopter 
        WHERE adopter_del_ind = FALSE"""

        values = []

        cols = ['ID #', 'Adopter Name', 'Age', 'Sex', 'Mobile No.', 'Address', 'Occupation']

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:

            #Create the Select link
            linkcolumn = {}
            for i, r in df.iterrows():
                linkcolumn[i] = dbc.Button(
                    "Select",
                    href = '/schedule/adopt?mode=select&adopterid='+str(r['ID #']),
                    id = {
                        'type': 'dynamic_adopter_id_select', 
                        'index': str(r['ID #'])
                        },
                    n_clicks = 0
                    )

            # Name of column of hyperlinks
            dictionarydata = {'Action': linkcolumn}

            data_dict = df.to_dict()
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)

            df = df[['ID #', 'Adopter Name', 'Age', 'Sex', 'Mobile No.', 'Address', 'Occupation', 'Action']]

            df.sort_values(by='ID #', inplace = True)
            df.drop(columns=['ID #'], inplace = True)

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                        hover=True, size='xl')

        if df.shape[0]:
            return [table]
        else:
            return ["No values to show here."]

    else:
        raise PreventUpdate

# Select Adopter of Interest from list
@app.callback(
    [
        Output('adoption_name', 'value'),
        Output('adoption_age', 'value'),
        Output('adoption_l', 'value'),
        Output('adoption_no', 'value'),
        Output('adoption_s', 'value'),
        Output('adoption_occ', 'value')
    ],
    [
        Input({'type': 'dynamic_adopter_id_select', 'index': ALL}, 'n_clicks')
    ],
    [
        State('url', 'search')
    ]
)
def selectadopterofinterest(adopterselected, search):
    ctx = dash.callback_context
    if ctx.triggered:

        event = ctx.triggered[0]['prop_id'].split('.')[0]
        event = json.loads(event)
        eventid = event["type"]

        if eventid == 'dynamic_adopter_id_select' and adopterselected:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'view':
                no_update = dash.no_update

                return [no_update, no_update, no_update, 
                    no_update, no_update, no_update]
                
            elif mode == 'select':

                adopter_id = parse_qs(parsed.query)['adopterid'][0]

                sql = """
                SELECT adopter_m, adopter_a, adopter_l, adopter_no, adopter_s, adopter_occ
                FROM adopter
                WHERE adopter_n = %s
                """

                values = [adopter_id]

                cols = ['Name', 'Age', 'Address', 'Number', 'Sex', 'Occupation']

                df_adopter = db.querydatafromdatabase(sql, values, cols)

                adopter_name = df_adopter['Name'][0]
                adopter_age = df_adopter['Age'][0]
                adopter_address = df_adopter['Address'][0]
                adopter_number = df_adopter['Number'][0]
                adopter_sex = df_adopter['Sex'][0]
                adopter_occ = df_adopter['Occupation'][0]

                return [adopter_name, adopter_age, adopter_address,
                adopter_number, adopter_sex, adopter_occ]
            
            else:
                raise PreventUpdate

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

# Record New Adopter
@app.callback(
    [
        Output('adopter_addalert', 'color'),
        Output('adopter_addalert', 'children'),
        Output('adopter_addalert', 'is_open'),
        Output('adopter_addsuccessmodal', 'is_open')
    ],
    [
        Input('sub_adopter', 'n_clicks'),
        Input('adopter_close_button', 'n_clicks')
    ],
    [
        State('adopter_name', 'value'),
        State('adopter_age', 'value'),
        State('adopter_l', 'value'),
        State('adopter_no', 'value'),
        State('adopter_s', 'value'),
        State('adopter_occ', 'value'),
        State('url', 'search')
    ]
)
def submit_adoptrinfo(submitbtn, closebtn, adoptrm, adoptra, adoptrl, adoptrno, adoptrs, adoptrocc, search):
    ctx = dash.callback_context # ctx filter ensures only change in url will activate this callback
    if ctx.triggered:
        event_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if event_id == 'sub_adopter' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click 
            # and not by having the submit button appear in the layout

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # Required entries – insert later
            if not adoptrm:
                alert_open = True
                alert_color = 'danger'
                alert_text = """Check your inputs. Kindly supply the adopter's name."""

            elif not adoptra:
                alert_open = True
                alert_color = 'danger'
                alert_text = """Check your inputs. Kindly supply the adopter's age."""

            else:
                
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                print(create_mode)
                
                # Add Section
                if create_mode == 'add':

                    sql_check = """
                    SELECT adopter_m as NAME, adopter_a as AGE, adopter_s as SEX, adopter_no as NUMBER,
                    adopter_l as LOCATION, adopter_occ as OCCUPATION
                    FROM adopter
                    """

                    values_check = []

                    cols = ['NAME', 'AGE', 'SEX', 'NUMBER', 'LOCATION', 
                            'OCCUPATION']

                    df = db.querydatafromdatabase(sql_check, values_check, cols)

                    # initialize ID numbers
                    adopter_id = 1
                    adopter_transid = 1

                    if len(df) == 0:
                        adopter_id = 1
                        adopter_transid = 1
                    else:
                        adopter_id = len(df) + 1
                        adopter_transid = len(df) + 1

                    adopter_date_entr = datetime.now().strftime("%Y-%m-%d")

                    sql_add = """
                    INSERT INTO adopter(adopter_n, adopter_m, adopter_a, adopter_s, adopter_no, adopter_l, adopter_occ, adopter_date_entr, adopter_transid, adopter_del_ind)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values_add = [adopter_id, adoptrm, adoptra, adoptrs, 
                    adoptrno, adoptrl, adoptrocc, adopter_date_entr, adopter_transid, False]

                    db.modifydatabase(sql_add, values_add)

                    modal_open = True

                    return [alert_color, alert_text, alert_open, modal_open]
                
                elif create_mode == 'edit':
                    
                    # Obtain adopter id
                    adopter_id = int(parse_qs(parsed.query)['adopterid'][0])

                    # Generate SQL script

                    sql = """
                    UPDATE adopter
                    SET
                        adopter_m = %s,
                        adopter_a = %s,
                        adopter_l = %s,
                        adopter_no = %s,
                        adopter_occ = %s
                    WHERE
                        adopter_n = %s"""

                    values = [adoptrm, adoptra, adoptrl, adoptrno, adoptrocc, adopter_id]

                    db.modifydatabase(sql, values)

                    modal_open = True

                    return [alert_color, alert_text, alert_open, modal_open]
                
                else:
                    raise PreventUpdate

        elif event_id == 'adopter_close_button' and closebtn:

            modal_open = False
            alert_color = ''
            alert_text = ''
            alert_open = False
            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

#%%

# Adopter-related (Adopter Database)

# Show Adopter Table
@app.callback(
    [
        Output('adopter_table', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def adoptertable(pathname):
    if pathname == '/adoptions/adopter_list':

        # Obtain records from SQL
        sql = """
        SELECT adopter_n, adopter_m, adopter_a, adopter_s, 
        adopter_no, adopter_l, adopter_occ 
        FROM adopter 
        WHERE adopter_del_ind = FALSE"""

        values = []

        cols = ['ID #', 'Adopter Name', 'Age', 'Sex', 'Mobile No.', 'Address', 'Occupation']

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:
            #Creating the hyperlinks
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        'Edit',
                                        href='/adoptions?mode=edit&adopterid='+str(row['ID #']),
                                        id = {
                                            'type': 'edit_adopter',
                                            'index': str(row['ID #'])
                                            },
                                        n_clicks = 0
                                ),

                                    width=1
                                ),

                                dbc.Col(
                                    dbc.Button(
                                    'Delete',
                                    href='/adoptions/adopter_list?mode=delete&adopterid='+str(row['ID #']),
                                    id = {
                                        'type': 'delete_adopter',
                                        'index': str(row['ID #'])
                                        },
                                    n_clicks = 0
                                    ),
                                    width={'size': 2, 'offset': 2}
                                )
                            ]
                        )
                    ]
                )
            
            # Name the column of hyperlinks - Action
            dictionarydata = {'Action': linkcolumn}

            data_dict = df.to_dict()
            data_dict.update(dictionarydata)

            df = pd.DataFrame.from_dict(data_dict)

            df = df[['ID #', 'Adopter Name', 'Age', 'Sex', 'Mobile No.', 'Address', 'Occupation', 'Action']]

            df.sort_values(by='ID #', inplace = True)
            df.drop(columns=['ID #'], inplace = True)

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                        hover=True, size='sm',
                        style = {
                            'whiteSpace': 'normal',
                            'height': 'auto'
                        })
        
        if df.shape[0]:
            return [table]
        else:
            return ['No records to display.']
        
    else:
        raise PreventUpdate

# adopter_data_store is the variable name that represents data to indicate any changes in it

# Edit Adopter: Update Data Store Variable
@app.callback(
    [
        Output('adopter_data_store', 'data')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url','search')
    ]
)
def edit_adopter_entry_dsv(pathname, search):
    if pathname == '/adoptions':
        # Check if we're in add or edit mode

        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]

        adopter_data = 1 if create_mode == 'edit' else 0

        return [adopter_data]

    else:
        raise PreventUpdate

# Edit Adopter: Reflect Change in Data Store
@app.callback(
    [
        Output('adopter_name', 'value'),
        Output('adopter_age', 'value'),
        Output('adopter_l', 'value'),
        Output('adopter_no', 'value'),
        Output('adopter_s', 'value'),
        Output('adopter_occ', 'value'),
        # Output('adopter_modal_message', 'children') ## consider updating this in a future update
    ],
    [
        Input('adopter_data_store', 'modified_timestamp') # Reflect change in adopter_data_store edit
    ],
    [
        State('adopter_data_store', 'data'),
        State('url', 'search')
    ]
)
def edit_adopter_entry_reflect(timestamp, data, search):
    print("data status:", data)
    if data:
        
        # Get adopter id
        parsed = urlparse(search)
        adopter_id = int(parse_qs(parsed.query)['adopterid'][0])

        # Query from DB
        sql = """
            SELECT adopter_m, adopter_a, adopter_l, adopter_no, adopter_s, adopter_occ FROM adopter
            WHERE adopter_n = %s
        """
        
        values = [adopter_id]

        cols = ['adopter_name', 'adopter_age', 'adopter_address', 'adopter_no', 'adopter_s', 'adopter_occ']

        df = db.querydatafromdatabase(sql, values, cols)
        print(df)

        adopter_name = df['adopter_name'][0]
        adopter_age = df['adopter_age'][0]
        adopter_address = df['adopter_address'][0]
        adopter_number = df['adopter_no'][0]
        adopter_sex = df['adopter_s'][0]
        adopter_occ = df['adopter_occ'][0]

        return [adopter_name, adopter_age, adopter_address, adopter_number, adopter_sex, adopter_occ]
        
    else:
        raise PreventUpdate

# Delete Adopter
@app.callback(
    [
        Output('adopter_delsuccessmodal', 'is_open')
    ],
    [
        Input({'type': 'delete_adopter', 'index': ALL}, 'n_clicks'),
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def delete_adopter_entry(selectedadopter, pathname, search):
    if pathname == '/adoptions/adopter_list':
        ctx = dash.callback_context
        if ctx.triggered:

            event = ctx.triggered[0]['prop_id'].split('.')[0] # {"index":"5","type":"delete_adopter"}
            event = json.loads(event) # {'index': '5', 'type': 'delete_adopter'}

            eventid = event["type"]
            

            if eventid == 'delete_adopter' and selectedadopter:
                parsed = urlparse(search)

                if not parsed.query:
                    raise PreventUpdate
                
                elif parsed.query:
                    mode = parse_qs(parsed.query)['mode'][0]

                    if not mode:
                        return [dash.no_update]

                    elif mode == 'delete':
                
                        adopter_id = parse_qs(parsed.query)['adopterid'][0]

                        sql = """
                        UPDATE adopter
                        SET adopter_del_ind = True
                        WHERE adopter_n = %s"""

                        values = [adopter_id]

                        db.modifydatabase(sql, values)

                        return [True]

                    raise PreventUpdate
            else:
                raise PreventUpdate
        
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# Refresh after deleting
# Developer's note: This might be compiled with other delete options
# @app.callback(
#     [
#         Output('url', 'href')
#     ],
#     [
#         Input('adopter_delsuccessmodal', 'is_open'),
#         Input('delmed_successmodal', 'is_open')
#     ]
# )
# def refresh_adopter_database(openstatus_adopter, openstatus_medicine):
#     if openstatus_adopter == True:
#         time.sleep(1)
#         url = '/adoptions/adopter_list'
#         return [url]

#     elif openstatus_medicine == True:
#         time.sleep(1)
#         url = '/medicine'
#         return [url]
    
#     else:
#         raise PreventUpdate

#%%

# Adopter-related (Adoption History)

# Show List of Pending Adoptions
@app.callback(
    [
        Output('adoptionhistory_table', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('url', 'search'),
        Input('adoption_success', 'n_clicks'),
        Input('adoption_pending', 'n_clicks'),
        Input('adoption_fail', 'n_clicks'),
    ]
)
def show_adoption_history(pathname, search, successbtn, pendingbtn, failbtn):
    if pathname == '/adoptions/history':
        ctx = dash.callback_context
        if ctx.triggered:

            parsed = urlparse(search)
            history_mode = parse_qs(parsed.query)['mode'][0]

            print('history mode:', history_mode)

            if history_mode == 'success' and successbtn:

                sql = """
                SELECT a.adopt_order_n, ad.adopter_m, ad.adopter_l, ad.adopter_no, 
                p.pet_m, p.pet_b, p.pet_s, a.adopt_order_r, a.adopt_order_c, a.adopt_order_trans_date
                from adoption a INNER JOIN pet p ON p.pet_n = a.pet_n
                INNER JOIN adopter ad ON a.adopter_n = ad.adopter_n
                WHERE adopt_order_del_ind = False
                AND pet_delete_ind = True and pet_adpt_stat = True
                AND adopt_order_r = %s
                """

                values = ['Y']

                cols = ['Adopt Order #', 'Adopter Name', 'Adopter Address', 'Adopter No.',
                'Pet Name', 'Pet Breed', 'Pet Sex', 'Result', 'Adoption Cost', 'Transaction Date']

                main_df = db.querydatafromdatabase(sql, values, cols)

                if main_df.shape[0]:

                    linkcolumn = {}
                    for index, row in main_df.iterrows():

                        linkcolumn[index] = html.Div(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        dbc.Button(
                                            "View Result",
                                            href='/adoptions/history?mode=success&func=review&orderid='+str(row['Adopt Order #']),
                                            id = {
                                                'type': 'view_success',
                                                'index': str(row['Adopt Order #'])
                                            },
                                            n_clicks = 0
                                            ),
                                    )
                                )
                            ]
                        )
                    
                    dictionarydata = {'Action': linkcolumn}

                    data_dict = main_df.to_dict()
                    data_dict.update(dictionarydata)

                    main_df = pd.DataFrame.from_dict(data_dict)

                    main_df = main_df[['Adopt Order #', 'Adopter Name', 'Adopter Address', 'Adopter No.',
                    'Pet Name', 'Pet Breed', 'Pet Sex', 'Result', 'Adoption Cost', 'Transaction Date', 'Action']]

                    main_df.sort_values(by='Adopt Order #', inplace = True)
                    main_df.drop(columns=['Result'], inplace = True)
                    # table_df.drop(columns=['Adopt Order #'], inplace = True)

                table = dbc.Table.from_dataframe(main_df, striped=True, bordered=True,
                                hover=True, size='sm')

                if main_df.shape[0]:
                    return [table]
                else:
                    return ['No records to display.']

            elif history_mode == 'pending' and pendingbtn:

                # Include date of rescue
                sql = """
                SELECT a.adopt_order_n, ad.adopter_m, ad.adopter_l, ad.adopter_no, 
                p.pet_m, p.pet_b, p.pet_s, ai.adopt_order_inq_a, ai.adopt_order_inq_b, ai.adopt_order_inq_c,
                ai.adopt_order_inq_d, ai.adopt_order_inq_e, a.adopt_order_r, a.adopt_order_c
                from adoption a INNER JOIN adoptioninquiry ai
                ON a.adopt_order_inq_n = ai.adopt_order_inq_n
                INNER JOIN pet p ON p.pet_n = a.pet_n
                INNER JOIN adopter ad ON a.adopter_n = ad.adopter_n
                WHERE adopter_del_ind = False AND adopt_order_del_ind = False
                AND pet_delete_ind = False and pet_adpt_stat = True
                AND adopt_order_r = %s
                """

                values = ['P']

                cols = ['Adopt Order #', 'Adopter Name', 'Adopter Address', 'Adopter No.',
                'Pet Name', 'Pet Breed', 'Pet Sex', 'Reason 1', 'Reason 2', 'Reason 3', 'Reason 4', 'Reason 5', 'Result', 'Adoption Cost']

                main_df = db.querydatafromdatabase(sql, values, cols)

                # table_df = main_df['Adopt Order #', 'Adopter Name', 'Adopter Address', 'Adopter No.',
                # 'Pet Name', 'Pet Breed', 'Pet Sex', 'Adoption Cost']

                #2. Create the html element to return to the Div

                if main_df.shape[0]: #if rows in the dataframe > 0

                    linkcolumn = {}
                    for index, row in main_df.iterrows():
                        linkcolumn[index] = html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                'View Answers',
                                                href = '/adoptions/history?mode=pending&func=review&orderid='+str(row['Adopt Order #']),
                                                id = {
                                                    'type': 'view_answers',
                                                    'index': str(row['Adopt Order #'])
                                                    },
                                                n_clicks = 0
                                            )
                                        ),

                                        dbc.Col(
                                            dbc.Button(
                                                'Update',
                                                href = '/adoptions/history?mode=pending&func=update&orderid='+str(row['Adopt Order #']),
                                                id = {
                                                    'type': 'update_adoption_order',
                                                    'index': str(row['Adopt Order #'])
                                                },
                                                n_clicks = 0
                                            )
                                        )
                                    ],

                                    justify='evenly'
                                )
                            ]
                        )
                    
                    # Name the column of hyperlinks - Action
                    dictionarydata = {'Action': linkcolumn}

                    data_dict = main_df.to_dict()
                    data_dict.update(dictionarydata)

                    main_df = pd.DataFrame.from_dict(data_dict)

                    main_df = main_df[['Adopt Order #', 'Adopter Name', 'Adopter Address', 'Adopter No.',
                    'Pet Name', 'Pet Breed', 'Pet Sex', 'Result', 'Adoption Cost', 'Action']]

                    main_df.sort_values(by='Adopt Order #', inplace = True)
                    main_df.drop(columns=['Result'], inplace = True)
                    # table_df.drop(columns=['Adopt Order #'], inplace = True)

                table = dbc.Table.from_dataframe(main_df, striped=True, bordered=True,
                                hover=True, size='sm')

                if main_df.shape[0]:
                    return [table]
                else:
                    return ['No records to display.']

            elif history_mode == 'fail' and failbtn:
               
                sql = """
                SELECT a.adopt_order_n, ad.adopter_m, ad.adopter_l, ad.adopter_no, 
                p.pet_m, p.pet_b, p.pet_s, a.adopt_order_r, a.adopt_order_c
                from adoption a
                INNER JOIN pet p ON p.pet_n = a.pet_n
                INNER JOIN adopter ad ON a.adopter_n = ad.adopter_n
                WHERE adopt_order_del_ind = False
                AND adopt_order_r = %s
                """

                values = ['F']

                cols = ['Adopt Order #', 'Adopter Name', 'Adopter Address', 'Adopter No.',
                'Pet Name', 'Pet Breed', 'Pet Sex', 'Result', 'Adoption Cost']

                main_df = db.querydatafromdatabase(sql, values, cols)

                print(main_df)
                
                if main_df.shape[0]:

                    linkcolumn = {}
                    for index, row in main_df.iterrows():
                        linkcolumn[index] = [
                            dbc.Row(
                                dbc.Col(
                                    dbc.Button(
                                        "View Result",
                                        href='/adoptions/history?mode=fail&func=review&orderid='+str(row['Adopt Order #']),
                                        id = {
                                            'type': 'view_failed',
                                            'index': str(row['Adopt Order #'])
                                        },
                                        n_clicks = 0
                                        ),
                                )
                            )
                        ]
                    
                    dictionarydata = {'Action': linkcolumn}

                    data_dict = main_df.to_dict()
                    data_dict.update(dictionarydata)

                    main_df = pd.DataFrame.from_dict(data_dict)

                    main_df = main_df[['Adopt Order #', 'Adopter Name', 'Adopter Address', 'Adopter No.',
                    'Pet Name', 'Pet Breed', 'Pet Sex', 'Result', 'Adoption Cost', 'Action']]

                    main_df.sort_values(by='Adopt Order #', inplace = True)
                    main_df.drop(columns=['Result'], inplace = True)
                    main_df.drop(columns=['Adoption Cost'], inplace = True)

                table = dbc.Table.from_dataframe(main_df, striped=True, bordered=True,
                                hover=True, size='sm')

                if main_df.shape[0]:
                    return [table]
                else:
                    return ['No records to display.']
            else:
                raise PreventUpdate

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# Show View Answers Module
@app.callback(
    [
        Output('interview_modal_window', 'is_open'),
        Output('interview_q_a', 'children'),
        Output('interview_q_b', 'children'),
        Output('interview_q_c', 'children'),
        Output('interview_q_d', 'children'),
        Output('interview_q_e', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input({'type': 'view_success', 'index': ALL}, 'n_clicks'),
        Input({'type': 'view_answers', 'index': ALL}, 'n_clicks'),
        Input({'type': 'view_failed', 'index': ALL}, 'n_clicks'),
    ],
    [
        State('url', 'search'),
    ]
)
def view_answers(pathname, successanswer, pendinganswer, failedanswer, search):
    if pathname == '/adoptions/history':
        ctx = dash.callback_context
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            event = json.loads(eventid)
            event_type = event['type']

            parsed = urlparse(search)

            if len(parse_qs(parsed.query)) == 1:
                raise PreventUpdate

            else:

                if event_type == 'view_answers' and pendinganswer:
            
                    mode = parse_qs(parsed.query)['func'][0]

                    if not mode:
                        raise PreventUpdate

                    elif mode == 'review':
                        orderid = parse_qs(parsed.query)['orderid'][0]
                
                        # SQL
                        sql = """
                        SELECT * from adoptioninquiry
                        WHERE adopt_order_inq_n = %s"""

                        values = [orderid]

                        cols = ['Order #', 'A', 'B', 'C', 'D', 'E']

                        df = db.querydatafromdatabase(sql, values, cols)

                        return [True, df['A'], df['B'], df['C'], df['D'], df['E']]

                    else:
                        raise PreventUpdate
                
                if event_type == 'view_success' and successanswer:
            
                    mode = parse_qs(parsed.query)['func'][0]

                    if not mode:
                        raise PreventUpdate

                    elif mode == 'review':
                        orderid = parse_qs(parsed.query)['orderid'][0]
                
                        # SQL
                        sql = """
                        SELECT * from adoptioninquiry
                        WHERE adopt_order_inq_n = %s"""

                        values = [orderid]

                        cols = ['Order #', 'A', 'B', 'C', 'D', 'E']

                        df = db.querydatafromdatabase(sql, values, cols)

                        return [True, df['A'], df['B'], df['C'], df['D'], df['E']]

                    else:
                        raise PreventUpdate
                
                if event_type == 'view_failed' and failedanswer:
            
                    mode = parse_qs(parsed.query)['func'][0]

                    if not mode:
                        raise PreventUpdate

                    elif mode == 'review':
                        orderid = parse_qs(parsed.query)['orderid'][0]
                
                        # SQL
                        sql = """
                        SELECT * from adoptioninquiry
                        WHERE adopt_order_inq_n = %s"""

                        values = [orderid]

                        cols = ['Order #', 'A', 'B', 'C', 'D', 'E']

                        df = db.querydatafromdatabase(sql, values, cols)

                        return [True, df['A'], df['B'], df['C'], df['D'], df['E']]

                    else:
                        raise PreventUpdate

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

# Show Update Modal
@app.callback(
    [
        Output('update_interview_results', 'is_open'),
        Output('modal_adopter_name', 'children'),
        Output('modal_pet_name', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input({'type': 'update_adoption_order', 'index': ALL}, 'n_clicks')
    ],
    [
        State('url', 'search')
    ]
)
def show_update_modal(pathname, updatebtn, search):
    if pathname == '/adoptions/history':
        ctx = dash.callback_context
        no_update = dash.no_update
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            event = json.loads(eventid)
            event_type = event['type']

            parsed = urlparse(search)
            print(parsed)

            if len(parse_qs(parsed.query)) <= 1:
                raise PreventUpdate

            else:
                if event_type == 'update_adoption_order' and updatebtn:

                    mode = parse_qs(parsed.query)['func'][0]

                    if not mode:
                        raise PreventUpdate

                    elif mode == 'update':
                        orderid = parse_qs(parsed.query)['orderid'][0]

                        sql = """
                        SELECT a.adopt_order_n, ad.adopter_m, p.pet_m from adoption a INNER JOIN adopter ad
                        ON ad.adopter_n = a.adopter_n INNER JOIN pet p ON p.pet_n = a.pet_n
                        WHERE adopt_order_n = %s
                        """

                        values = [orderid]

                        cols = ['Order #', 'Adopter', 'Pet']

                        df = db.querydatafromdatabase(sql, values, cols)

                        return [True, df['Adopter'], df['Pet']]
                    
                    else:
                        raise PreventUpdate

                else:
                    raise PreventUpdate
        else:
            raise PreventUpdate
                    
    else:
        raise PreventUpdate

# Update Order Request
@app.callback(
    [
        Output('adoption_history_alert', 'is_open'),
        Output('adoption_history_alert', 'color'),
        Output('adoption_history_alert', 'children'),
        Output('register_adopt_order', 'is_open')
    ],
    [
        Input('url', 'pathname'),
        Input('submit_adoption_order', 'n_clicks')
    ],
    [
        State('url', 'search'),
        State('adoption_cost', 'value'),
        State('adoption_order_result_dropdown', 'value'),
        State('trans_date', 'date')
    ]
)
def update_order_request(pathname, submitbtn, search, adoptioncost, adoptionresult, dateoftrans):
    if pathname == '/adoptions/history':
        ctx = dash.callback_context # ctx filter ensures only change in url will activate this callback
        if ctx.triggered:
            event_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if event_id == 'submit_adoption_order' and submitbtn:

                parsed = urlparse(search)
                orderid = parse_qs(parsed.query)['orderid'][0]

                alert_open = False
                modal_open = False
                alert_color = ''
                alert_text = ''

                # Alert Text won't show up
                if not adoptionresult:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = 'Please select a result before proceeding.'

                    return [alert_color, alert_text, alert_open, modal_open]

                if adoptionresult == 'F':

                    if not dateoftrans:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Please input the date of transaction.'

                        return [alert_open, alert_color, alert_text, modal_open]

                    # SQL for adoption
                    sql = """
                    UPDATE adoption
                    SET adopt_order_trans_date = %s,
                    adopt_order_r = %s
                    WHERE adopt_order_n = %s"""

                    values = [dateoftrans, adoptionresult, orderid]

                    db.modifydatabase(sql, values)

                    modal_open = True

                    return [alert_open, alert_color, alert_text, modal_open]

                    # SQL for pet? (maybe put this in the success tab instead)
                
                elif adoptionresult == 'Y':

                    if not dateoftrans:
                        alert_open = True
                        alert_color = 'danger'
                        alert_text = 'Please input the date of transaction.'

                        return [alert_open, alert_color, alert_text, modal_open]

                    # SQL for adoption
                    sql_adpt = """
                    UPDATE adoption
                    SET adopt_order_trans_date = %s,
                    adopt_order_r = %s,
                    adopt_order_c = %s
                    WHERE adopt_order_n = %s"""

                    values_adpt = [dateoftrans, adoptionresult, adoptioncost, orderid]

                    db.modifydatabase(sql_adpt, values_adpt)

                    # SQL for pet ==> for the success tab, show pets even with the deleted condition
                        # Query Adoption SQL to Obtain Pet ID
                    sql_pet = """
                    SELECT pet_n from adoption
                    WHERE adopt_order_n = %s"""
                    values_pet = [orderid]
                    cols_pet = ['Pet #']
                    df = db.querydatafromdatabase(sql_pet, values_pet, cols_pet)

                        # Modify Pet SQL
                    sql_pet_adpt = """
                    UPDATE pet
                    SET pet_delete_ind = %s
                    WHERE pet_n = %s
                    """
                    values_pet_adpt = [True, df['Pet #'][0].item()] # Bug?

                    db.modifydatabase(sql_pet_adpt, values_pet_adpt)

                    modal_open = True

                    return [alert_open, alert_color, alert_text, modal_open]
                
                elif adoptionresult == 'P':

                    # Update cost and date of transaction

                    # SQL for adoption
                    sql = """
                    UPDATE adoption
                    SET adopt_order_trans_date = %s,
                    adopt_order_r = %s,
                    adopt_order_c = %s
                    WHERE adopt_order_n = %s"""

                    values = [dateoftrans, adoptionresult, adoptioncost, orderid]

                    db.modifydatabase(sql, values)

                    modal_open = True

                    return [alert_open, alert_color, alert_text, modal_open]

            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

#%% ANIMAL CARE

    # Adopt an Animal

# Select Pet for Adopt Entry
# This is connected to the dataframe imported into pet_data
@app.callback(
    [
        Output('pet_adoptionlist', 'options')
    ],
    [
        Input('adminshelter_data', 'data')
    ]
)
def adoptevent_petdropdown(shelterdata):

    shelter_data_df = pd.DataFrame.from_records(shelterdata)

    sql_pet = """
                SELECT pet_n, pet_m, pet_b, pet_s, pet_adpt_stat, shelter_n FROM pet
                WHERE pet_delete_ind = FALSE
                AND pet_adpt_stat = TRUE
                AND shelter_n = %s
                AND NOT EXISTS (SELECT 1
                                FROM adoption
                                WHERE adoption.pet_n = pet.pet_n
                                AND adopt_order_r ILIKE 'P' AND 'Y')
                """
    
    values_pet = [int(shelter_data_df.at[0, 'SHELTER ID'])]

    cols_pet = ['ID #', 'Name', 'Breed', 'Sex', 'Ready for Adoption?', 'Shelter #']

    pet_df_available = db.querydatafromdatabase(sql_pet, values_pet, cols_pet)

    # Drop down – pet name / breed / sex – (value: id/name)
    options_petdropdown = []
    for index, row in pet_df_available.iterrows():
        option = {}
        option['label'] = '{} / {} / {}'.format(row['Name'], row['Breed'], row['Sex'])
        option['value'] = '{}'.format(row['ID #'])
        options_petdropdown.append(option)

    return [options_petdropdown]

# Show pet value in Adopt Entry
@app.callback(
    [
        Output('pet_adoptselectdiv', 'hidden'),
        Output('pet_adoptselectresult_name', 'children'),
        Output('pet_adoptselectresult_breed', 'children'),
        Output('pet_adoptselectresult_sex', 'children'),
        Output('pet_adoptselectresult_rs', 'children')
    ],
    [
        Input('pet_adoptionlist', 'value')
    ]
)
def adoptevent_petselected(pet):
    if not pet:
        raise PreventUpdate
    else:

        sql = """
        SELECT pet_m, pet_b, pet_s, pet_rs FROM pet
        WHERE pet_n = %s
        AND pet_delete_ind = False"""

        values = [pet]

        cols = ['Name', 'Breed', 'Sex', 'Rescue Story']

        df = db.querydatafromdatabase(sql, values, cols)

        name_result = "Name: {}".format(df.loc[0, 'Name'])
        breed_result = "Breed: {}".format(df.loc[0, 'Breed'])
        sex_result = "Sex: {}".format(df.loc[0, 'Sex'])
        rs_result = df.loc[0, 'Rescue Story']

        return [False, name_result, breed_result, sex_result, rs_result]

# Submit Adoption Order
@app.callback(
    [
        Output('adoption_addalert', 'color'),
        Output('adoption_addalert', 'children'),
        Output('adoption_addalert', 'is_open'),
        Output('adoption_addsuccessmodal', 'is_open')
    ],
    [
        Input('adminshelter_data', 'data'),
        Input('sub_adoption', 'n_clicks'),
        Input('adoption_close_button', 'n_clicks')
    ],
    [
        State('adoption_name', 'value'),
        State('adoption_age', 'value'),
        State('adoption_l', 'value'),
        State('adoption_no', 'value'),
        State('adoption_s', 'value'),
        State('adoption_occ', 'value'),
        State('pet_adoptionlist', 'value'),
        State('aoq_ppl_amt', 'value'),
        State('aoq_idealpet', 'value'),
        State('aoq_allergycount', 'value'),
        State('aoq_petownership', 'value'),
        State('aoq_steps', 'value')
    ]
)
def submitadoptionorder(shelterdata, submitbtn,
    closebtn, adoptername, adopterage, adopterloc,
    adopterno, adoptersex, adopterocc, adoptlist, aoqamt, aoqideal,
    aoqallergy, aoqpetown, aoqsteps):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'sub_adoption' and submitbtn:
        
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            sql_check = """
            SELECT adopt_order_n from adoption
            WHERE adopt_order_del_ind = FALSE
            """

            values_check = []

            cols = ['ORDER #']

            df = db.querydatafromdatabase(sql_check, values_check, cols)

            adopt_order_id = 1
            adopt_order_inq_id = 1

            if len(df) == 0:
                adopt_order_id = 1
                adopt_order_inq_id = 1
            elif len(df) > 0:
                adopt_order_id = len(df) + 1
                adopt_order_inq_id = len(df) + 1

            shelter_data_df = pd.DataFrame.from_records(shelterdata)

            shelter_id = int(shelter_data_df.at[0, 'SHELTER ID'])

            # Get adopter id
            sql_adopter = """
            SELECT adopter_n
            FROM adopter
            WHERE adopter_del_ind = False
            AND adopter_m = %s
            AND adopter_s = %s
            AND adopter_a = %s
            AND adopter_l = %s
            AND adopter_no = %s
            AND adopter_occ = %s"""

            values_adopter = [adoptername, adoptersex, adopterage, adopterloc,
                    adopterno, adopterocc]

            cols_adopter = ['ID #']

            adopter_df = db.querydatafromdatabase(sql_adopter, values_adopter, cols_adopter)

            adopter_id = int(adopter_df.at[0, 'ID #'])

            adopt_order_r = 'P'

            # Add to Adoption Order Inquiry Table
            adoption_inq_sql = """
            INSERT INTO adoptioninquiry(adopt_order_inq_n, adopt_order_inq_a, adopt_order_inq_b, adopt_order_inq_c, adopt_order_inq_d, adopt_order_inq_e)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            adoption_inq_values = [adopt_order_inq_id, aoqamt, aoqideal, aoqallergy, aoqpetown, aoqsteps]

            db.modifydatabase(adoption_inq_sql, adoption_inq_values)

            # Add to Adoption Database
            adoptionsql_add = """
            INSERT INTO adoption(adopt_order_n, adopt_order_inq_n, adopt_order_r, pet_n, adopter_n, shelter_n, adopt_order_del_ind)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            adoptionvalues_add = [adopt_order_id, adopt_order_inq_id, adopt_order_r, adoptlist, adopter_id, shelter_id, False]

            db.modifydatabase(adoptionsql_add, adoptionvalues_add)

            modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]

        elif eventid == 'adoption_close_button' and closebtn:

            modal_open = False
            alert_color = ''
            alert_text = ''
            alert_open = False
            return [alert_color, alert_text, alert_open, modal_open]            

        else:
            raise PreventUpdate
        
    else:
        raise PreventUpdate
 
# Task for today
# timestamps!

if __name__=='__main__':

    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)

# %%

