package com.example.taskmanagement.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;

import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name ="tasks")
@Data
@NoArgsConstructor
@AllArgsConstructor

public class Task{
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)

private Long id;

private string title;

private string description;

private boolean completed;



}