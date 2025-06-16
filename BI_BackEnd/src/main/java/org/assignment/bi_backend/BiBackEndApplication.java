package org.assignment.bi_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EnableJpaRepositories(basePackages = "org.assignment.bi_backend.Repository")
@EntityScan(basePackages = "org.assignment.bi_backend.Entity")
public class BiBackEndApplication {

    public static void main(String[] args) {
        SpringApplication.run(BiBackEndApplication.class, args);
    }

}
