# Типы 

## Task

```typescript
{
    id:number,
    time:string
}
```
## Category

```typescript
{
    name:String,
    code:String
}
```
## SubTask

```typescript
{
    id:number,
    userCategories:[Category],
    defaultCategories:  [Category],
    isValid: boolean
}
```

# API

## POST /api/express

### Request

```typescript
{
    headers:{
        "Content-Type": "application/json"
    },
    body:{
        name: str
        codes:[Number]
    }
}
```

### Response 
```typescript
{
    сategories:[Category],
    isValid: boolean
}
```


## POST /api/tasks

### Request

```typescript
{
    headers:{
        "Content-Type": "multipart/form-data",
    },
    body:{
        file:blob
    }
}
```

### Response

```typescript
{
    task: Task
}
```
## GET /api/tasks?skip=Number&take=Number

### Response
```typescript
{
    tasks:[Task]
}
```
## GET  /api/tasks/:id?skip=Number&take=Number

### Response
```typescript
{
    subTasks:[SubTask]
}
```