package org.intb.repositories;

import org.intb.entity.Blob;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BlobRepository extends JpaRepository<Blob, Long> {
}
