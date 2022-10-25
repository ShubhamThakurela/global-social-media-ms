from app.main.database.connector import db_connection, CREDENTIALS


def prepare_update(org_data, data_id):
    expression = ""
    data_tuple = ()
    for key, value in org_data.items():
        data_tuple = data_tuple + (value,)
        expression += key + "=%s, "

    data_tuple = data_tuple + (data_id,)
    return data_tuple, expression.strip(", ")


def prepare_insert(org_data):
    expression_col = ""
    expression_val = ""
    data_tuple = ()
    for key, value in org_data.items():
        data_tuple = data_tuple + (value,)
        expression_col += key + ", "
        expression_val += "%s, "

    return data_tuple, expression_col.strip(", "), expression_val.strip(", ")


def insert_update_scraping_detail(org_data):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT profile_id FROM {}.social_media_scraping_details WHERE company_name='{}'".format(
            CREDENTIALS['DATABASE'], org_data['company_name']))
        s_detail = cursor.fetchone()
        if s_detail:
            sd_id = s_detail[0]
            update_data, expression = prepare_update(org_data, sd_id)
            query = "UPDATE " + CREDENTIALS[
                'DATABASE'] + ".social_media_scraping_details SET " + expression + " WHERE profile_id=%s"
            cursor.execute(query, update_data)
        else:
            insert_data, expression_col, expression_val = prepare_insert(org_data)
            query = "INSERT INTO " + CREDENTIALS[
                'DATABASE'] + ".social_media_scraping_details (" + expression_col + ") VALUES (" + expression_val + ")"
            cursor.execute(query, insert_data)
            sd_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return sd_id
    except Exception as e:
        print(str(e))
        return None


def prepare_updates(linkedin_data_dict, data_id):
    expression = ""
    data_tuple = ()
    for key, value in linkedin_data_dict.items():
        data_tuple = data_tuple + (value,)
        expression += key + "=%s, "

    data_tuple = data_tuple + (data_id,)
    return data_tuple, expression.strip(", ")


def prepare_inserts(linkedin_data_dict):
    expression_col = ""
    expression_val = ""
    data_tuple = ()
    for key, value in linkedin_data_dict.items():
        data_tuple = data_tuple + (value,)
        expression_col += key + ", "
        expression_val += "%s, "

    return data_tuple, expression_col.strip(", "), expression_val.strip(", ")


def insert_update_linkedin_scrapped_data(linkedin_data_dict):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        # cursor.execute("SELECT company_id FROM {}.social_media_scraping_details WHERE company_name='{}'".format(CREDENTIALS['DATABASE'], org_data['company_name']))
        cursor.execute(
            "SELECT profile_id FROM {}.linkedin_scrapped_data WHERE Company_Name='{}'".format(CREDENTIALS['DATABASE'],
                                                                                              linkedin_data_dict[
                                                                                                  'Company_Name']))
        s_detail = cursor.fetchone()
        if s_detail:
            profile_id = s_detail[0]
            update_data, expression = prepare_updates(linkedin_data_dict, profile_id)
            query = "UPDATE " + CREDENTIALS[
                'DATABASE'] + ".linkedin_scrapped_data SET " + expression + " WHERE profile_id=%s"
            cursor.execute(query, update_data)
        else:
            insert_data, expression_col, expression_val = prepare_inserts(linkedin_data_dict)
            query = "INSERT INTO " + CREDENTIALS[
                'DATABASE'] + ".linkedin_scrapped_data (" + expression_col + ") VALUES (" + expression_val + ")"
            cursor.execute(query, insert_data)  #
            profile_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return profile_id
    except Exception as e:
        print(str(e))
        return {"status": "Data Not Inserted"}


def prepare_updatess(pitchbook_dict, data_id):
    expression = ""
    data_tuple = ()
    for key, value in pitchbook_dict.items():
        data_tuple = data_tuple + (value,)
        expression += key + "=%s, "

    data_tuple = data_tuple + (data_id,)
    return data_tuple, expression.strip(", ")


def prepare_insertss(pitchbook_dict):
    expression_col = ""
    expression_val = ""
    data_tuple = ()
    for key, value in pitchbook_dict.items():
        data_tuple = data_tuple + (value,)
        expression_col += key + ", "
        expression_val += "%s, "

    return data_tuple, expression_col.strip(", "), expression_val.strip(", ")


def insert_update_pitchbook_scrapped_data(pitchbook_dict):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        # cursor.execute("SELECT company_id FROM {}.social_media_scraping_details WHERE company_name='{}'".format(CREDENTIALS['DATABASE'], org_data['company_name']))
        cursor.execute(
            "SELECT profile_id FROM {}.pitchbook_scrapped_data WHERE Company_Name='{}'".format(CREDENTIALS['DATABASE'],
                                                                                               pitchbook_dict[
                                                                                                   'company_name']))
        s_detail = cursor.fetchone()
        if s_detail:
            profile_id = s_detail[0]
            update_data, expression = prepare_updates(pitchbook_dict, profile_id)
            query = "UPDATE " + CREDENTIALS[
                'DATABASE'] + ".pitchbook_scrapped_data SET " + expression + " WHERE profile_id=%s"
            cursor.execute(query, update_data)
        else:
            insert_data, expression_col, expression_val = prepare_inserts(pitchbook_dict)
            query = "INSERT INTO " + CREDENTIALS[
                'DATABASE'] + ".pitchbook_scrapped_data (" + expression_col + ") VALUES (" + expression_val + ")"
            cursor.execute(query, insert_data)
            profile_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return profile_id
    except Exception as e:
        print(str(e))
        return {"status": "Data Not Inserted"}


# def get_source(source):
#     try:
#         connection = db_connection()
#         cursor = connection.cursor()
#         query = ("SELECT source_url FROM social_media_scraping_details WHERE source='linkedin'".format(
#             CREDENTIALS['DATABASE'], source))
#         cursor.execute(query)
#         result = cursor.fetchone()
#         source_url = result[0] if result else None
#         connection.close()
#         return source_url
#     except Exception as e:
#         print(str(e))
#         return None


def get_data_linkedin(org_url):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM linkedin_scrapped_data WHERE Source_Url= '%s'"
        # parameter into query using % symbol
        final_query = (query % org_url)
        cursor.execute(final_query)
        result = cursor.fetchone()
        connection.close()
        return result
    except Exception as e:
        print(str(e))
        return None


def get_data_pitchbook(url):
    try:
        connection = db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM pitchbook_scrapped_data WHERE Source_Url= '%s'"
        # parameter into query using % symbol
        final_query = (query % url)
        cursor.execute(final_query)
        result = cursor.fetchone()
        connection.close()
        return result
    except Exception as e:
        print(str(e))
        return None
