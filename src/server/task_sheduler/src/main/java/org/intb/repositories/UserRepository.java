package org.intb.repositories;

import org.intb.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
    // Additional custom methods can be defined here if needed
}