from fastapi import FastAPI
import psycopg2
from dotenv import dotenv_values

from ViewModels.VmGetUsers import vm_get_users
from ViewModels.VmGetUserID import vm_get_user_id
from ViewModels.VmAddUser import vm_add_user
from ViewModels.VmUpdateUser import vm_apdate_user


config = dotenv_values(".env")

connect = psycopg2.connect(
    host=config["HOST"],
    port=config["PORT"],
    user=config["USER_ID"],
    password=config["USER_PW"],
    database=config["DB_Name"]
)

cursor = connect.cursor()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Processing successful"}


# 5. Обновить данные

@app.put("/update")
def update_user(user: vm_apdate_user):
    try:
        cursor.execute(f"""
            UPDATE users
            SET name = '{user.name}', lastName = '{user.lastName}', birthday = '{user.birthday}', city = '{user.city}', country = '{user.country}', eMail = '{user.eMail}'
            WHERE id = {user.id};
        """)
        connect.commit()

        return {"message": "Success"}
    except Exception as e:
        return {"error": e}


@app.patch("/patch-user")
def patch_user(user: vm_apdate_user):
    try:
        cursor.execute(f"""
            UPDATE users
            SET name = '{user.name}', eMail = '{user.eMail}'
            WHERE id = {user.id};
        """)
        connect.commit()

        return {"message": "Success"}
    except Exception as e:
        return {"error": e}




# 4. Добавление пользователя

@app.post("/add-user")
def add_user(user: vm_add_user):
    try:
        cursor.execute(f"""
            INSERT INTO users (id, name, lastName, birthday, city, country, eMail)
            VALUES ('{user.id}', '{user.name}', '{user.lastName}', '{user.birthday}', '{user.city}', '{user.country}', '{user.eMail}');
        """)
        connect.commit()

        return {"message": "Success"}
    except Exception as e:
        return {"error": e}




# 3. Удалить пользователя по ID

@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    try:
        cursor.execute(f"""
            DELETE FROM users
            WHERE id = {user_id};
        """)
        connect.commit()

        return {"message": "Success"}
    except Exception as e:
        return {"error": e}



# 2. Получить данные пользователя по ID

@app.get("/get-user/{id}")
def get_user(id: int):
    try:
        cursor.execute(f"""
            SELECT id, name, lastName, birthday, city, country, eMail
            FROM users 
            WHERE id = {id};
        """)
        result = cursor.fetchone()
        user = (vm_get_user_id(
            id=result[0],
            name=result[1],
            lastName=result[2],
            birthday=result[3],
            city=result[4],
            country=result[5],
            eMail=result[6],
        ))

        return {"user": user}
    except Exception as e:
        return {"error": e}




# 1. Получить все данные таблицы user
#
# @app.get("/get-all-users")
# def get_all_users():
#     try:
#         cursor.execute("SELECT * FROM users")
#         result = cursor.fetchall()
#         list_users = []
#         for i in result:
#             list_users.append(vm_get_users({"id": i[0], "name": i[1], "lastName": i[2], "birthday": i[3], "city": i[4], "country": i[5], "eMail": i[6]}))
#
#         return {"users": list_users}
#     except Exception as e:
#         print(e)
#         return {"error": e}


@app.get("/get-users")
def get_users():
    try:
        cursor.execute("""
        SELECT id, name, lastName, birthday, city, country, eMail
        FROM users;
        """)
        result = cursor.fetchall()
        list_users = []
        # print(result[0])
        for i in result:
            # print(list_users)
            list_users.append(vm_get_users(
                id=i[0],
                name=i[1],
                lastName=i[2],
                birthday=i[3],
                city=i[4],
                country=i[5],
                eMail=str(i[6])
            ))

        return {"users": list_users}
    except Exception as e:
        return {"error": e}


