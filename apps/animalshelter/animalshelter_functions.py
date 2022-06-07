   # Shelter Schedule Functions

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

# Show Consent Form
@app.callback(
    [
        Output('consent_form', 'is_open'),
        Output('consent_form', 'autofocus')
    ],
    [
        Input('consent_form_click', 'n_clicks')
    ]
)
def open_consent_form(consentclick):
    if consentclick:
        consent_modal = True
        modal_focus = True
        return [consent_modal, modal_focus]
    else:
        raise PreventUpdate

    # Schedule Event Functions

    ## Situationer

# Animal Care Select
# Add switch button here, activate Adopter Appointment button
@app.callback(
    [
        Output('animalcare_selectmodal', 'is_open'),
        Output('animalcare_selectmodal', 'autoFocus'),
        Output('animal_situationer', 'hidden'),
        Output('animal_vetappointment', 'hidden'),
        Output('sched_interviewappointment', 'hidden')
    ],
    [
        Input('animal_situationerbtn', 'n_clicks'),
        Input('animal_vetappointmentbtn', 'n_clicks'),
        Input('animal_adptrappointmentbtn', 'n_clicks')
    ]
)
def animalcarelayout(situationerbtn, vetappointmentbtn, adptrappointmentbtn):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'animal_situationerbtn' and situationerbtn:
            select_modal = False
            modal_focus = False
            situationer_layout = False
            appointment_layout = True
            interview_layout = True

            return [select_modal, modal_focus, situationer_layout, appointment_layout, interview_layout]

        elif eventid == 'animal_vetappointmentbtn' and vetappointmentbtn:
            select_modal = False
            modal_focus = False
            situationer_layout = True
            appointment_layout = False
            interview_layout = True

            return [select_modal, modal_focus, situationer_layout, appointment_layout, interview_layout]

        elif eventid == 'animal_adptrappointmentbtn' and adptrappointmentbtn:
            select_modal = False
            modal_focus = False
            situationer_layout = True
            appointment_layout = True
            interview_layout = False

            return [select_modal, modal_focus, situationer_layout, appointment_layout, interview_layout]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# Submit Situationer Details
@app.callback(
    [
        Output('situationer_addalert', 'color'),
        Output('situationer_addalert', 'children'),
        Output('situationer_addalert', 'is_open'),
        Output('sit_addsuccessmodal', 'is_open')
    ],
    [
        Input('adminshelter_data', 'data'),
        Input('sub_sit', 'n_clicks'),
        Input('continue_sitaddrecord', 'n_clicks')
    ],
    [
        State('sit_d', 'date'),
        State('sit_animalcount', 'value'),
        State('sit_location', 'value')
    ]
)
def submitsituationer(admindata, submitbtn, closebtn, situationerdate, sitcount, sitloc):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'sub_sit' and submitbtn:

            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False

            if not situationerdate:
                alert_color = 'danger'
                alert_text = 'Please provide the date of situationer.'
                alert_open = True
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]

            elif not sitloc:
                alert_color = 'danger'
                alert_text = 'Please provide the location of situationer.'
                alert_open = True
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]

            elif not sitcount:
                alert_color = 'danger'
                alert_text = 'Please provide the number of expected rescues.'
                alert_open = True
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]

            else:
                # Parameters for Event Type and Admin ID            
                event_type_n = 1

                admin_df = pd.DataFrame.from_records(admindata)
                admin_id = int(admin_df.at[0, 'ADMIN ID'])

                # Check Situationer Length
                sql_check_sit = """
                SELECT * from eventsituationer
                WHERE situationer_del_ind = False"""

                values_check_sit = []

                cols = ['Sit ID', 'Event ID', 'Expected Rescues', 'Location', 'Deleted?']

                df_sit = db.querydatafromdatabase(sql_check_sit, values_check_sit, cols)

                situationer_n = 1

                if len(df_sit) == 0:
                    situationer_n = 1
                elif len(df_sit) != 0:
                    situationer_n = len(df_sit) + 1

                # Get Event DF
                sql_check_events = """
                SELECT event_n from event
                WHERE event_del_ind = False"""

                values_check_events = []

                cols_events = ['Event ID']

                df_events = db.querydatafromdatabase(sql_check_events, values_check_events, cols_events)

                events_len = len(df_events)

                event_id = 1

                if events_len == 0:
                    event_id = 1
                elif events_len != 0:
                    event_id = events_len + event_id

                # Get Schedule DF
                sql_check_sch = """
                SELECT schedule_n from schedule
                WHERE schedule_del_ind = False"""

                values_check_sch = []

                cols_sch = ['Schedule ID']

                df_sch = db.querydatafromdatabase(sql_check_sch, values_check_sch, cols_sch)

                sch_len = len(df_sch)

                sch_id = 1

                if sch_len == 0:
                    sch_id = 1
                elif sch_len != 0:
                    sch_id = sch_len + sch_id

                # Add Event
                event_result = "Pending"
                event_name = "Situationer"

                add_event_sql = """
                INSERT INTO event(event_n, admin_n, event_m, event_type_n, event_r, event_del_ind)
                VALUES (%s, %s, %s, %s, %s, %s)"""

                add_event_values = [event_id, admin_id, event_name, event_type_n, event_result, False]

                db.modifydatabase(add_event_sql, add_event_values)

                # Add Event Situationer
                add_event_sit_sql = """
                INSERT INTO eventsituationer(situationer_n, event_n, situationer_anml_rsc, situationer_l, situationer_del_ind)
                VALUES (%s, %s, %s, %s, %s)"""

                add_event_sit_values = [situationer_n, event_id, sitcount, sitloc, False]

                db.modifydatabase(add_event_sit_sql, add_event_sit_values)

                # Add Schedule
                add_sch_sql = """
                INSERT INTO schedule(schedule_n, event_n, schedule_d, schedule_del_ind)
                VALUES (%s, %s, %s, %s)"""

                add_sch_values = [sch_id, event_id, situationerdate, False]

                db.modifydatabase(add_sch_sql, add_sch_values)

                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]     

        elif eventid == 'continue_apptaddrecord' and closebtn:

            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False
            
            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

# Schedule Interview
# event_type_n = 3
# event_name = "Adopter Interview"
@app.callback(
    [
        Output('interview_addalert', 'color'),
        Output('interview_addalert', 'children'),
        Output('interview_addalert', 'is_open'),
        Output('interview_addsuccessmodal', 'is_open')
    ],
    [
        Input('adminshelter_data', 'data'),
        Input('submit_interviewappointment', 'n_clicks'),
        Input('continue_interviewaddrecord', 'n_clicks')
    ],
    [
        State('interview_d', 'date'),
        State('adpt_interviewlist', 'value')
    ]
)
def animalcare_scheduleinterview(shelterdata, submitbtn, continuebtn, interviewdate, adopterselected):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'submit_interviewappointment' and submitbtn:

            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False

            if not interviewdate:
                alert_color = 'danger'
                alert_text = 'Please provide a date.'
                alert_open = True

                return [alert_color, alert_text, alert_open, modal_open]

            if not adopterselected:
                alert_color = 'danger'
                alert_text = 'Please select an adopter.'
                alert_open = True

                return [alert_color, alert_text, alert_open, modal_open]
            
            event_type_n = 3
            admin_df = pd.DataFrame.from_records(shelterdata)
            admin_id = int(admin_df.at[0, 'ADMIN ID'])

            # Get EventInterview DF
            sql_check_int = """
            SELECT * from eventinterview
            WHERE interview_del_ind = False
            """

            values_check_int = []

            cols = ['Interview ID', 'Event ID', 'Selected Adopter', 'Deleted?']

            df_int = db.querydatafromdatabase(sql_check_int, values_check_int, cols)

            interview_n = 1

            if len(df_int) == 0:
                interview_n = 1
            elif len(df_int) != 0:
                interview_n = len(df_int) + 1

            # Get Event DF
            sql_check_events = """
            SELECT event_n from event
            WHERE event_del_ind = False"""

            values_check_events = []

            cols_events = ['Event ID']

            df_events = db.querydatafromdatabase(sql_check_events, values_check_events, cols_events)

            events_len = len(df_events)

            event_id = 1

            if events_len == 0:
                event_id = 1
            elif events_len != 0:
                event_id = events_len + event_id

            # Get Schedule DF
            sql_check_sch = """
            SELECT schedule_n from schedule
            WHERE schedule_del_ind = False"""

            values_check_sch = []

            cols_sch = ['Schedule ID']

            df_sch = db.querydatafromdatabase(sql_check_sch, values_check_sch, cols_sch)

            sch_len = len(df_sch)

            sch_id = 1

            if sch_len == 0:
                sch_id = 1
            elif sch_len != 0:
                sch_id = sch_len + sch_id

            # Add Event
            event_result = "Pending"
            event_name = "Adopter Interview" # Change later by either removing this column in SQL or merge with event type

            add_event_sql = """
            INSERT INTO event(event_n, admin_n, event_m, event_type_n, event_r, event_del_ind)
            VALUES (%s, %s, %s, %s, %s, %s)"""

            add_event_values = [event_id, admin_id, event_name, event_type_n, event_result, False]

            db.modifydatabase(add_event_sql, add_event_values)

            # Add Event Interview
            add_event_int_sql = """
            INSERT INTO eventinterview(interview_n, event_n, adopter_n, interview_del_ind)
            VALUES (%s, %s, %s, %s)"""

            add_event_int_values = [interview_n, event_id, adopterselected, False]

            db.modifydatabase(add_event_int_sql, add_event_int_values)

            # Add Schedule
            add_sch_sql = """
            INSERT INTO schedule(schedule_n, event_n, schedule_d, schedule_del_ind)
            VALUES (%s, %s, %s, %s)"""

            add_sch_values = [sch_id, event_id, interviewdate, False]

            db.modifydatabase(add_sch_sql, add_sch_values)

            modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]

        elif eventid == 'continue_interviewaddrecord' and continuebtn:

            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False

            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# Dropdown: Adopter Interview - Select Adopter
# Select Adopter with a Currently Scheduled Interview
@app.callback(
    [
        Output('adpt_interviewlist', 'options')
    ],
    [
        Input('adminshelter_data', 'data')
    ]
)
def animalcare_adopterlist(shelterdata):
    shelter_data_df = pd.DataFrame.from_records(shelterdata)

    sql_adptr = """
    SELECT adopter_n, adopter_m, adopter_s, adopter_no, adopter_a from adopter
    WHERE adopter_del_ind = False
    """

    values_adptr = []

    cols_adptr = ['ID #', 'Name', 'Sex', 'Number', 'Age']

    adopter_df = db.querydatafromdatabase(sql_adptr, values_adptr, cols_adptr)

    # Drop down – value: id/name
    options_adopterintdropdown = []
    for index, row in adopter_df.iterrows():
        option = {}
        option['label'] = '{} / {} / {} / {} '.format(row['Name'], row['Age'], 
                            row['Sex'], row['Number'])
        option['value'] = '{}'.format(row['ID #'])
        options_adopterintdropdown.append(option)

    return [options_adopterintdropdown]

# Dropdown: Vet – Vet Examination
@app.callback(
    [
        Output('vet_examinationlist', 'options')
    ],
    [
        Input('adminshelter_data', 'data')
    ]
)
def animalcare_vetdropdown(shelterdata):

    shelter_data_df = pd.DataFrame.from_records(shelterdata)

    sql_vet = """
    SELECT vet_n, vet_m, vet_a, vet_spec, vet_sal, vet_no from veterinarian
    WHERE vet_del_ind = False
    AND shelter_n = %s"""

    values_vet = [int(shelter_data_df.at[0, 'SHELTER ID'])]

    cols_vet = ['VET #', 'Name', 'Age', 'Specialization', 'Salary', 'Number']

    vet_df = db.querydatafromdatabase(sql_vet, values_vet, cols_vet)

    # Drop down – value: id/name
    options_vetexamdropdown = []
    for index, row in vet_df.iterrows():
        option = {}
        option['label'] = '{} / {} / {} / {} / {}'.format(row['Name'], row['Age'], 
                            row['Specialization'], row['Salary'], row['Number'])
        option['value'] = '{}'.format(row['VET #'])
        options_vetexamdropdown.append(option)

    return [options_vetexamdropdown]

# Dropdown: Pet – Vet Examination
@app.callback(
    [
        Output('pet_examinationlist', 'options')
    ],
    [
        Input('adminshelter_data', 'data')
    ]
)
def animalcare_petdropdown(shelterdata):

    shelter_data_df = pd.DataFrame.from_records(shelterdata)

    sql_pet = """
    SELECT pet_n, pet_m, pet_b, pet_s from pet
    WHERE pet_delete_ind = False
    AND shelter_n = %s
    AND pet_adpt_stat = False"""

    pet_values = [int(shelter_data_df.at[0, 'SHELTER ID'])]

    pet_cols = ['ID #', 'Name', 'Breed', 'Sex']

    pet_df = db.querydatafromdatabase(sql_pet, pet_values, pet_cols)

    # Obtain SQL values

    # Drop down – pet name / breed / sex – (value: id/name
    options_petdropdown = []
    for index, row in pet_df.iterrows():
        option = {}
        option['label'] = '{} / {} / {}'.format(row['Name'], row['Breed'], row['Sex'])
        option['value'] = '{}'.format(row['ID #'])
        options_petdropdown.append(option)

    return [options_petdropdown]

# Show pet details on dropdown
@app.callback(
    [
        Output('pet_medicalrecorddiv', 'hidden'),
        Output('pet_medicalrecordexam', 'children')
    ],
    [
        Input('pet_examinationlist', 'value')
    ]
)
def animalcare_showpetmr(pet):
    if not pet:
        raise PreventUpdate
    else:

        sql = """
        SELECT pet_mr FROM pet
        WHERE pet_n = %s"""

        values = [pet]

        cols = ['Medical Records']

        df = db.querydatafromdatabase(sql, values, cols)

        pet_mr = df.loc[0, 'Medical Records']

        return [False, pet_mr]

# Submit Veterinary Check-Up Detals
@app.callback(
    [
        Output('appointment_addalert', 'color'),
        Output('appointment_addalert', 'children'),
        Output('appointment_addalert', 'is_open'),
        Output('appt_addsuccessmodal', 'is_open')
    ],
    [
        Input('adminshelter_data', 'data'),
        Input('submit_vetappointment', 'n_clicks'),
        Input('continue_apptaddrecord', 'n_clicks')
    ],
    [
        State('vetappt_d', 'date'),
        State('pet_examinationlist', 'value'),
        State('vet_examinationlist', 'value'),
    ]
)
def animalcare_submitappointment(admindata, submitbtn, closebtn,
                    vetdate, petdetails, vetdetails):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'submit_vetappointment' and submitbtn:

            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False

            if not vetdate:
                alert_color = 'danger'
                alert_text = 'Please provide the date of appointment.'
                alert_open = True
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]

            elif not petdetails:
                alert_color = 'danger'
                alert_text = 'Please select the pet of interest.'
                alert_open = True
                modal_open = False
            
                return [alert_color, alert_text, alert_open, modal_open]
            elif not vetdetails:
                alert_color = 'danger'
                alert_text = 'Please select a veterinarian.'
                alert_open = True
                modal_open = False

                return [alert_color, alert_text, alert_open, modal_open]
            else:

                # Parameters for Event Type and Admin ID            
                event_type_n = 2

                admin_df = pd.DataFrame.from_records(admindata)
                admin_id = int(admin_df.at[0, 'ADMIN ID'])

                # Check Visit DF
                sql_check_vetappt = """
                SELECT * from eventcheckup
                """

                values_check_vetappt = []

                cols = ['Check UP ID', 'Event ID', 'Vet ID', 'Pet ID', 'Deleted?']

                df_appt = db.querydatafromdatabase(sql_check_vetappt, values_check_vetappt, cols)

                check_up_n = 1

                if len(df_appt) == 0:
                    check_up_n = 1
                elif len(df_appt) != 0:
                    check_up_n = len(df_appt) + 1

                # Get Event DF
                sql_check_events = """
                SELECT event_n from event
                WHERE event_del_ind = False"""

                values_check_events = []

                cols_events = ['Event ID']

                df_events = db.querydatafromdatabase(sql_check_events, values_check_events, cols_events)

                events_len = len(df_events)

                event_id = 1

                if events_len == 0:
                    event_id = 1
                elif events_len != 0:
                    event_id = events_len + event_id

                # Get Schedule DF
                sql_check_sch = """
                SELECT schedule_n from schedule
                WHERE schedule_del_ind = False"""

                values_check_sch = []

                cols_sch = ['Schedule ID']

                df_sch = db.querydatafromdatabase(sql_check_sch, values_check_sch, cols_sch)

                sch_len = len(df_sch)

                sch_id = 1

                if sch_len == 0:
                    sch_id = 1
                elif sch_len != 0:
                    sch_id = sch_len + sch_id

                # Add Event
                event_result = "Pending"
                event_name = "Veterinary Checkup" # Change later by either removing this column in SQL or merge with event type

                add_event_sql = """
                INSERT INTO event(event_n, admin_n, event_m, event_type_n, event_r, event_del_ind)
                VALUES (%s, %s, %s, %s, %s, %s)"""

                add_event_values = [event_id, admin_id, event_name, event_type_n, event_result, False]

                db.modifydatabase(add_event_sql, add_event_values)

                # Add Event Situationer
                add_event_sit_sql = """
                INSERT INTO eventcheckup(check_up_n, event_n, vet_n, pet_n, check_up_del_ind)
                VALUES (%s, %s, %s, %s, %s)"""

                add_event_sit_values = [check_up_n, event_id, vetdetails, petdetails, False]

                db.modifydatabase(add_event_sit_sql, add_event_sit_values)

                # Add Schedule
                add_sch_sql = """
                INSERT INTO schedule(schedule_n, event_n, schedule_d, schedule_del_ind)
                VALUES (%s, %s, %s, %s)"""

                add_sch_values = [sch_id, event_id, vetdate, False]

                db.modifydatabase(add_sch_sql, add_sch_values)

                modal_open = True
    
                return [alert_color, alert_text, alert_open, modal_open]
        elif eventid == 'continue_apptaddrecord' and closebtn:
            alert_color = ''
            alert_text = ''
            alert_open = False
            modal_open = False

            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
