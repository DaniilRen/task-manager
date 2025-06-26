package org.intb.response.task;

import org.intb.entity.User;
import org.intb.response.AbstractResponse;

import java.util.List;

public class GetUserResponse extends AbstractResponse {

    private Long userId;

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

}
