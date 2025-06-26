package org.intb.response.task;

import org.intb.entity.User;
import org.intb.response.AbstractResponse;

import java.util.List;

public class ListUsersResponse extends AbstractResponse {

    private List<User> users;

    public List<User> getUsers() {
        return users;
    }

    public void setUsers(List<User> users) {
        this.users = users;
    }
}
