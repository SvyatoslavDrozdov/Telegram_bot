import sqlite3

G = 6.674301515151515 * 10 ** (-11)
M_sun = 1.98847 * 10 ** 30


def perihelion(a, e):
    v_p = G * M_sun * (1 + e) / (a * (1 - e))
    v_p = v_p ** 0.5
    return v_p


conn = sqlite3.connect("database.db")
cur = conn.cursor()

# cur.execute("""DROP TABLE standard_obj""")
cur.execute(
    """CREATE TABLE IF NOT EXISTS standard_obj (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name varchar(50),
    x decimal,
    y decimal,
    v_x decimal,
    v_y decimal,
    end_time decimal
    )""")

Mercury_period = 87.97 * 24 * 60 * 60
Mercury_semi_major_axis = 57.909227e9
Mercury_eccentricity = 0.20563593
Mercury_v_p = perihelion(Mercury_semi_major_axis, Mercury_eccentricity)
Mercury_perihelion = 46.001e9
cur.execute("""INSERT INTO standard_obj (name, x, y, v_x, v_y, end_time)
            VALUES ("Меркурий", 	'%s', 0, 0,  '%s', '%s')""" % (Mercury_perihelion, Mercury_v_p, Mercury_period))

Earth_period = 365.25 * 24 * 60 * 60
Earth_semi_major_axis = 149.598261e9
Earth_eccentricity = 0.01671123
Earth_period_v_p = perihelion(Earth_semi_major_axis, Earth_eccentricity)
Earth_perihelion = 147.098290e9
cur.execute("""INSERT INTO standard_obj (name, x, y, v_x, v_y, end_time)
            VALUES ("Земля", 	'%s', 0, 0,  '%s', '%s')""" % (Earth_perihelion, Earth_period_v_p, Earth_period))

Mars_period = 686.98 * 24 * 60 * 60
Mars_semi_major_axis = 227.94382e9
Mars_eccentricity = 0.0933941
Mars_v_p = perihelion(Mars_semi_major_axis, Mars_eccentricity)
Mars_perihelion = 206.655e9
cur.execute("""INSERT INTO standard_obj (name, x, y, v_x, v_y, end_time)
            VALUES ("Марс", 	'%s', 0, 0,  '%s', '%s')""" % (Mars_perihelion, Mars_v_p, Mars_period))

cur.execute("""INSERT INTO standard_obj (name, x, y, v_x, v_y, end_time)
            VALUES ("Комета Галея", 5.24824e12, 0, 0, 0.9e3, 2209032000)""")

conn.commit()
cur.close()
conn.close()
