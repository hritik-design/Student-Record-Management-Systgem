import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from tkinter import Canvas

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Record Management System")
        self.root.geometry("1280x720+50+20")
        self.root.resizable(False, False)
        self.root.config(bg="#E8F0FE")

        header_canvas = Canvas(self.root, width=1280, height=100, bd=0, highlightthickness=0)
        header_canvas.pack(fill="x")
        for i in range(100):
            r = 77 + i
            g = 184 - int(i * 0.6)
            b = 130 + int(i * 0.15)
            color = f"#{max(0,min(255,r)):02x}{max(0,min(255,g)):02x}{max(0,min(255,b)):02x}"
            header_canvas.create_rectangle(0, i, 1280, i + 1, outline="", fill=color)
        header_canvas.create_text(640, 50, text="🎓 Student Record Management System",
                                  font=("Arial", 30, "bold"), fill="white")

        optFrame = tk.Frame(self.root, bd=4, relief="groove", bg="#f8faff")
        optFrame.place(width=320, height=550, x=40, y=130)

        tk.Label(optFrame, text="Options", bg="#f8faff", fg="#2b2b2b",
                 font=("Arial", 22, "bold")).pack(pady=10)

        self.create_buttons(optFrame)

        self.detFrame = tk.Frame(self.root, bd=6, relief="ridge", bg="#f9fbe7")
        self.detFrame.place(width=850, height=550, x=380, y=130)

        tk.Label(self.detFrame, text="📘 Student Records", bg="#f9fbe7",
                 font=("Arial", 22, "bold")).pack(pady=10)

        self.tabFun()
        self.currentFrame = None

    def create_buttons(self, frame):
        buttons = [
            ("➕ Add Student", self.addFrameFun),
            ("🔍 Search Student", self.searchFrameFun),
            ("✏️ Update Record", self.updFrameFun),
            ("📋 Show All", self.showAll),
            ("🗑️ Remove Student", self.delFrameFun)
        ]
        for text, cmd in buttons:
            b = tk.Button(frame, text=text, command=cmd, bg="#4caf50", fg="white",
                          activebackground="#388e3c", activeforeground="white",
                          font=("Arial", 14, "bold"), width=20, height=2, bd=0)
            b.pack(pady=8)
            b.bind("<Enter>", lambda e, b=b: b.config(bg="#43a047"))
            b.bind("<Leave>", lambda e, b=b: b.config(bg="#4caf50"))

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="260604", database="STUDENTREC2")
        self.cur = self.con.cursor()

    def tabFun(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))
        style.configure("Treeview", font=("Arial", 12), rowheight=26)

        tabFrame = tk.Frame(self.detFrame, bg="#f9fbe7")
        tabFrame.pack(fill="both", expand=True, padx=15, pady=15)

        x_scroll = tk.Scrollbar(tabFrame, orient="horizontal")
        y_scroll = tk.Scrollbar(tabFrame, orient="vertical")

        self.table = ttk.Treeview(tabFrame,
                                  columns=("uid", "name", "fname", "course", "cgpa"),
                                  xscrollcommand=x_scroll.set,
                                  yscrollcommand=y_scroll.set)
        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)
        x_scroll.pack(side="bottom", fill="x")
        y_scroll.pack(side="right", fill="y")

        self.table.heading("uid", text="UID")
        self.table.heading("name", text="Name")
        self.table.heading("fname", text="Father Name")
        self.table.heading("course", text="Course")
        self.table.heading("cgpa", text="CGPA")
        self.table["show"] = "headings"

        self.table.column("uid", width=100, anchor="center")
        self.table.column("name", width=180, anchor="w")
        self.table.column("fname", width=180, anchor="w")
        self.table.column("course", width=140, anchor="center")
        self.table.column("cgpa", width=80, anchor="center")
        self.table.pack(fill="both", expand=True)

        self.showAll()

    def close_current_frame(self):
        if self.currentFrame:
            self.currentFrame.destroy()
            self.currentFrame = None

    def addFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#e3f2fd")
        self.currentFrame.place(width=450, height=460, x=420, y=160)

        entries = [
            ("UID:", "uid"), ("Name:", "name"), ("Father Name:", "fname"),
            ("Course:", "course"), ("CGPA:", "cgpa")
        ]
        self.addVars = {}
        for i, (lbl, var) in enumerate(entries):
            tk.Label(self.currentFrame, text=lbl, font=("Arial", 14, "bold"),
                     bg="#e3f2fd").grid(row=i, column=0, padx=18, pady=10, sticky="w")
            e = tk.Entry(self.currentFrame, width=24, font=("Arial", 13))
            e.grid(row=i, column=1, padx=8, pady=10)
            self.addVars[var] = e

        tk.Button(self.currentFrame, text="✅ Register", command=self.addFun,
                  bg="#2196f3", fg="white", font=("Arial", 14, "bold"),
                  width=15).grid(row=len(entries), column=0, columnspan=2, pady=8)

        tk.Button(self.currentFrame, text="❌ Cancel", command=self.close_current_frame,
                  bg="red", fg="white", font=("Arial", 12, "bold"),
                  width=12).grid(row=len(entries)+1, column=0, columnspan=2, pady=6)

    def addFun(self):
        uid = self.addVars["uid"].get().strip()
        name = self.addVars["name"].get().strip()
        fname = self.addVars["fname"].get().strip()
        course = self.addVars["course"].get().strip()
        cgpa = self.addVars["cgpa"].get().strip()

        if not (uid and name and fname and course and cgpa):
            messagebox.showerror("Error", "⚠️ Please fill all input fields!")
            return

        try:
            self.dbFun()
            self.cur.execute("INSERT INTO student(uid, name, fname, course, cgpa) VALUES (%s, %s, %s, %s, %s)",
                             (uid, name, fname, course, cgpa))
            self.con.commit()
            messagebox.showinfo("Success", f"🎉 Student {name} (UID: {uid}) added!")
            self.close_current_frame()
            self.showAll()
            self.con.close()
        except pymysql.err.IntegrityError:
            messagebox.showerror("Error", f"UID {uid} already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def searchFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#e8f5e9")
        self.currentFrame.place(width=450, height=240, x=420, y=200)

        tk.Label(self.currentFrame, text="Search By:", font=("Arial", 13, "bold"), bg="#e8f5e9").grid(row=0, column=0, padx=18, pady=12, sticky="w")
        self.search_option = ttk.Combobox(self.currentFrame, width=20, values=("uid", "name", "course"), font=("Arial", 12))
        self.search_option.set("Select Option")
        self.search_option.grid(row=0, column=1, padx=8, pady=12)

        tk.Label(self.currentFrame, text="Value:", font=("Arial", 13, "bold"), bg="#e8f5e9").grid(row=1, column=0, padx=18, pady=12, sticky="w")
        self.search_value = tk.Entry(self.currentFrame, width=22, font=("Arial", 12))
        self.search_value.grid(row=1, column=1, padx=8, pady=12)

        tk.Button(self.currentFrame, text="🔎 Search", command=self.searchFun,
                  bg="#1976d2", fg="white", font=("Arial", 13, "bold"), width=14).grid(row=2, column=0, columnspan=2, pady=8)

        tk.Button(self.currentFrame, text="❌ Close", command=self.close_current_frame,
                  bg="red", fg="white", font=("Arial", 11, "bold"), width=12).grid(row=3, column=0, columnspan=2, pady=4)

    def searchFun(self):
        opt = self.search_option.get()
        val = self.search_value.get().strip()
        if not val:
            messagebox.showerror("Error", "Enter a value to search.")
            return
        try:
            self.dbFun()
            query = f"SELECT * FROM student WHERE {opt} LIKE %s"
            self.cur.execute(query, (f"%{val}%",))
            rows = self.cur.fetchall()
            self.table.delete(*self.table.get_children())
            if rows:
                for r in rows:
                    self.table.insert('', tk.END, values=r)
                messagebox.showinfo("Info", f"{len(rows)} record(s) displayed.")
            else:
                messagebox.showinfo("Info", "No record found.")
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def updFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#fff3e0")
        self.currentFrame.place(width=450, height=300, x=420, y=180)

        tk.Label(self.currentFrame, text="Field:", font=("Arial", 13, "bold"), bg="#fff3e0").grid(row=0, column=0, padx=18, pady=10, sticky="w")
        self.update_field = ttk.Combobox(self.currentFrame, width=20, values=("name", "course", "cgpa", "fname"), font=("Arial", 12))
        self.update_field.set("Select Field")
        self.update_field.grid(row=0, column=1, padx=8, pady=10)

        tk.Label(self.currentFrame, text="New Value:", font=("Arial", 13, "bold"), bg="#fff3e0").grid(row=1, column=0, padx=18, pady=10, sticky="w")
        self.update_value = tk.Entry(self.currentFrame, width=22, font=("Arial", 12))
        self.update_value.grid(row=1, column=1, padx=8, pady=10)

        tk.Label(self.currentFrame, text="UID:", font=("Arial", 13, "bold"), bg="#fff3e0").grid(row=2, column=0, padx=18, pady=10, sticky="w")
        self.update_uid = tk.Entry(self.currentFrame, width=22, font=("Arial", 12))
        self.update_uid.grid(row=2, column=1, padx=8, pady=10)

        tk.Button(self.currentFrame, text="✏️ Update", command=self.updFun,
                  bg="#f57c00", fg="white", font=("Arial", 13, "bold"), width=14).grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(self.currentFrame, text="❌ Close", command=self.close_current_frame,
                  bg="red", fg="white", font=("Arial", 11, "bold"), width=12).grid(row=4, column=0, columnspan=2, pady=4)

    def updFun(self):
        field = self.update_field.get()
        val = self.update_value.get().strip()
        uid = self.update_uid.get().strip()

        if field not in ("name", "course", "cgpa", "fname") or not val or not uid:
            messagebox.showerror("Error", "All fields required.")
            return
        try:
            self.dbFun()
            query = f"UPDATE student SET {field}=%s WHERE uid=%s"
            self.cur.execute(query, (val, uid))
            self.con.commit()
            if self.cur.rowcount:
                messagebox.showinfo("Success", f"Record updated for UID {uid}")
            else:
                messagebox.showinfo("Info", "No record matched that UID.")
            self.close_current_frame()
            self.showAll()
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def showAll(self):
        try:
            self.dbFun()
            self.cur.execute("SELECT * FROM student")
            data = self.cur.fetchall()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('', tk.END, values=i)
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def delFrameFun(self):
        self.close_current_frame()
        self.currentFrame = tk.Frame(self.root, bd=5, relief="ridge", bg="#fdecea")
        self.currentFrame.place(width=450, height=200, x=420, y=220)

        tk.Label(self.currentFrame, text="UID:", font=("Arial", 13, "bold"), bg="#fdecea").grid(row=0, column=0, padx=18, pady=24, sticky="w")
        self.uid_entry = tk.Entry(self.currentFrame, width=22, font=("Arial", 12))
        self.uid_entry.grid(row=0, column=1, padx=8, pady=24)

        tk.Button(self.currentFrame, text="🗑️ Delete", command=self.delFun,
                  bg="#d32f2f", fg="white", font=("Arial", 13, "bold"), width=14).grid(row=1, column=0, columnspan=2, pady=8)
        tk.Button(self.currentFrame, text="❌ Close", command=self.close_current_frame,
                  bg="gray", fg="white", font=("Arial", 11, "bold"), width=12).grid(row=2, column=0, columnspan=2, pady=4)

    def delFun(self):
        uid = self.uid_entry.get().strip()
        if uid == "":
            messagebox.showerror("Error", "UID cannot be empty")
            return
        if not messagebox.askyesno("Confirm", f"Delete student with UID {uid}?"):
            return
        try:
            self.dbFun()
            self.cur.execute("DELETE FROM student WHERE uid=%s", (uid,))
            self.con.commit()
            if self.cur.rowcount:
                messagebox.showinfo("Success", f"Student with UID {uid} removed.")
            else:
                messagebox.showinfo("Info", "No matching UID found.")
            self.close_current_frame()
            self.showAll()
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    StudentApp(root)
    root.mainloop()
