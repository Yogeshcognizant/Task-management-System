package com.example.taskmanagement;
import com.example.taskmanagement.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TaskManagementApplication implements CommandLineRunner{
   @Autowired
  private TaskService taskService;
  public static void main(String[] args){
  SpringApplication.run(TaskManagementApplication.class,args);
  }

  @Override
  public void run(String... args) throws Exception{
    System.out.println("Starting Flask scheduler...");
    taskService.startScheduler();
    System.out.println("schedule started successfully.");
  }

}
