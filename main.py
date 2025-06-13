
from database import init_db, get_connection

def register():
    username = input("Enter new username: ")
    password = input("Enter password: ")

    conn = get_connection()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(" Registration successful.\n")
    except:
        print(" Username already exists.\n")
    finally:
        conn.close()

def login():
    username = input("Username: ")
    password = input("Password: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
    row = cur.fetchone()
    conn.close()

    if row:
        print(f"\nWelcome, {username}!\n")
        return row[0]
    else:
        print(" Invalid credentials.\n")
        return None

def add_task(user_id):
    title = input("Task title: ")
    desc = input("Description: ")
    due = input("Due date (YYYY-MM-DD): ")
    priority = input("Priority (Low, Medium, High): ")

    conn = get_connection()
    conn.execute("INSERT INTO tasks (user_id, title, description, due_date, priority) VALUES (?, ?, ?, ?, ?)",
                 (user_id, title, desc, due, priority))
    conn.commit()
    conn.close()
    print("Task added.\n")

def view_tasks(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT task_id, title, is_completed FROM tasks WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(" No tasks found.\n")
        return

    print("\nYour Tasks:")
    for task_id, title, done in rows:
        status = "✓" if done else "✗"
        print(f"{task_id}: {title} [{status}]")
    print()

def complete_task(user_id):
    task_id = input("Enter task ID to mark as complete: ")

    conn = get_connection()
    conn.execute("UPDATE tasks SET is_completed=1 WHERE task_id=? AND user_id=?", (task_id, user_id))
    conn.commit()
    conn.close()
    print("Task marked complete.\n")

def delete_task(user_id):
    task_id = input("Enter task ID to delete: ")

    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE task_id=? AND user_id=?", (task_id, user_id))
    conn.commit()
    conn.close()
    print("Task deleted.\n")

def search_tasks(user_id):
    keyword = input("Search keyword: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT task_id, title FROM tasks WHERE user_id=? AND title LIKE ?", (user_id, f"%{keyword}%"))
    results = cur.fetchall()
    conn.close()

    print("\nSearch Results:")
    if results:
        for task_id, title in results:
            print(f"{task_id}: {title}")
    else:
        print("No matching tasks found.")
    print()

def main_menu(user_id):
    while True:
        print("++++++++ Menu  ++++++++++\n")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Logout")

        choice = input("Select an option: ")

        if choice == "1":
            add_task(user_id)
        elif choice == "2":
            view_tasks(user_id)
        elif choice == "3":
            complete_task(user_id)
        elif choice == "4":
            delete_task(user_id)
        elif choice == "5":
            search_tasks(user_id)
        elif choice == "6":
            print("\n")
            break
        else:
            print(" Invalid option.\n")

def main():
    init_db()

    while True:
        print("====== Task Management System ======")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        action = input("Choose an option: ")

        if action == "1":
            user_id = login()
            if user_id:
                main_menu(user_id)
        elif action == "2":
            register()
        elif action == "3":
            print(" Goodbye!")
            break
        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    main()
