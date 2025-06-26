package org.intb.requests.user;

public class AddUserRequest {
    // Define the structure of the incoming JSON request
    private String name;
    private String surname;
    private String thirdName;
    private String login;
    private String password;

    public String getLogin() {
        return login;
    }

    public String getPassword() {
        return password;
    }

    public String getName() {
        return name;
    }

    public String getSurname() {
        return surname;
    }

    public String getThirdName() {
        return thirdName;
    }
}

