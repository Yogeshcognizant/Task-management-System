package com.example.taskmanagement.service;

import com.example.taskmanagement.model.Task;
import com.example.taskmanagement.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;

import java.util.List;
import java.util.Optional;

@Service
public class TaskService {

 @Autowired
 private TaskRepository taskRepository;

 public List<Task> getAllTasks() {
 return taskRepository.findAll();
 }

 public Task createTask(Task task) {
 return taskRepository.save(task);
 }

 public Task updateTask(Long id, Task taskDetails) {
 Task task = taskRepository.findById(id)
 .orElseThrow(() -> new RuntimeException("Task not found"));

 task.setTitle(taskDetails.getTitle());
 task.setDescription(taskDetails.getDescription());
 task.setCompleted(taskDetails.isCompleted());

 return taskRepository.save(task);
 }

 public void deleteTask(Long id) {
 taskRepository.deleteById(id);
 }

//scheduler code

public void startScheduler(){
try{
process process= new ProcessBuilder("python","../backend-flask/app.py).start();
}

catch (IOException e){
e.printStackTrace();


}


}
}

