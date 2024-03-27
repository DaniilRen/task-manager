package org.intb.requests.user;

public class EditUserRequest {
    // Define the structure of the incoming JSON request
    private Long id;
    private String name;
    private String surname;
    private String thirdName;
    private String login;
    private String password;

    public Long getId() {
        return id;
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

    public String getLogin() {
        return login;
    }

    public String getPassword() {
        return password;
    }
}
