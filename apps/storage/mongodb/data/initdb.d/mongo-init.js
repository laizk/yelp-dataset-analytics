db = db.getSiblingDB("test_db");

db.createUser({
  user: "db_user",
  pwd: "password",
  roles: [
    {
      role: 'readWrite',
      db: 'test_db'
    },
  ],
});

db.createCollection("test_collection");

db.test_collection.insertMany([
  {
    projectId: "P001",
    name: "Customer Analytics Dashboard",
    owner: "Alice",
    status: "active",
    created_at: "2024-01-10",
    tasks: [
      { taskId: "T1", title: "Data Cleaning", assignee: "Bob", done: false },
      { taskId: "T2", title: "ETL Pipeline Setup", assignee: "Charlie", done: true }
    ]
  },
  {
    projectId: "P002",
    name: "Inventory Forecasting",
    owner: "David",
    status: "completed",
    created_at: "2023-12-02",
    tasks: [
      { taskId: "T1", title: "Collect SKU Data", assignee: "Erika", done: true },
      { taskId: "T2", title: "Train ML Model", assignee: "Frank", done: true }
    ]
  },
  {
    projectId: "P003",
    name: "Website Redesign",
    owner: "George",
    status: "on_hold",
    created_at: "2024-02-20",
    tasks: [
      { taskId: "T1", title: "UI Wireframes", assignee: "Helen", done: true },
      { taskId: "T2", title: "Frontend Migration", assignee: "Ian", done: false }
    ]
  },
  {
    projectId: "P004",
    name: "Mobile App Launch",
    owner: "Jane",
    status: "active",
    created_at: "2024-03-15",
    tasks: [
      { taskId: "T1", title: "Design Mockups", assignee: "Kevin", done: false },
      { taskId: "T2", title: "Push Notification Setup", assignee: "Laura", done: false }
    ]
  },
  {
    projectId: "P005",
    name: "Marketing Automation",
    owner: "Mike",
    status: "planning",
    created_at: "2024-04-01",
    tasks: [
      { taskId: "T1", title: "Email Workflow Draft", assignee: "Nina", done: false },
      { taskId: "T2", title: "CRM Integration", assignee: "Oscar", done: false }
    ]
  }
]);
