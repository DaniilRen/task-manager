package org.intb.repositories;

import org.intb.entity.Task;
import org.intb.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TaskRepository extends JpaRepository<Task, Long> {

}
