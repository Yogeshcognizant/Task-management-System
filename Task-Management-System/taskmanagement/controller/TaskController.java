package com.example.taskmanagement.controller;

import com.example.taskmanagement.model.Task;

import com.example.taskmanagemnet.service.TaskService;

import springframework.beans.factory.annotation.Autowired;

import springframework.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tasks")
@CrossOrigin(origins = "*")
public class TaskController{

@Autowired
private TaskService taskService;

@GetMapping
public List<Task> getAllTasks(){
return taskService.getAllTasks();
}

@PostMapping
public Task createTask(@RequestBody Task task){
return taskService.createTask(task);
}

@PutMapping("/{id}")
public Task updateTask(@PathVariable Long id,@RequestBody Task task)
{
return taskService.updateTask(id, task);
}

@DeleteMapping("/{id}")
public Task deleteTask(@PathVariable Long id)
{
return taskService.deleteTask(id);
}


}


