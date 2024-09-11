 <!DOCTYPE html>
<html>
<body>

<h1>Define class</h1>
    
    <!--
    Both GET and POST create an array (e.g. array( key1 => value1, key2 => value2, key3 => value3, ...)).
    This array holds key/value pairs, where keys are the names of the form controls and values are the
    input data from the user.
    As information sent from a form with the POST method is invisible to others (all names/values are
        embedded within the body of the HTTP request) and has no limits on the amount of information to send.
        POST is preferred.
        -->
        <form action = "Project2Post.php" method = "post">
        Name: <input type = "text" name = "name" id = "name">
        <br>
        Email: <input type = "text" name = "password" id = "email">
        <input type = "submit">
        </form>
        <br>
        
       
        

</body>
</html>

