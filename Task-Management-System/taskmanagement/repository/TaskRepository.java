package com.example.taskmanagement.repository;

import com.example.taskmanagement.model.Task;

import org.springframework.data.jpa.repository.JpaRepository;

import org.springframework.stereotype.Repository;

public interface TaskRepository extends JpaRepository<Task,Long>{
}
