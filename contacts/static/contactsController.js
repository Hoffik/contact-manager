
var app = angular.module('contactsApp', []); //'ngResource'

// https://www.consolelog.io/django-csrf-token-with-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
// Allow django templates and angular to co-exist
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller('ContactListCtrl', function($scope, $filter, $log, $http) { 

    $scope.loadContacts = function() {
        $http.get('/api/contacts/').catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function(response) {
            $scope.contacts = response.data;
        });
    };

    $scope.loadContacts();

    $scope.createContact = function(new_contact) {
        var data = $.param({
            firstname: new_contact.firstname,
            lastname: new_contact.lastname,
            address: new_contact.address,
            email: new_contact.email,
            phone: new_contact.phone,
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.post('/api/contacts/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.loadContacts();
            $scope.new_contact = undefined;            
            $scope.ContactForm.$setPristine();
            $scope.ContactForm.$setUntouched();
        });
    };

    $scope.deleteContact = function(contact) {
        return $http.delete('/api/contacts/' + contact.id + '/').catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.loadContacts();
        });
    };
});


app.controller('ContactDetailCtrl', function($scope, $filter, $log, $http, $httpParamSerializer){ 
    $scope.getContact = function(contact_id) {
        $http.get('/api/contacts/' + contact_id + '/').catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function(response) {
            $scope.contact = response.data;
        });
    };

    $scope.updateContact = function(contact) {
        var data = $.param({
            firstname: contact.firstname,
            lastname: contact.lastname,
            address: contact.address,
            email: contact.email,
            phone: contact.phone,
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.put('/api/contacts/' + contact.id + '/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.getContact($scope.contact.id);
            $scope.ContactForm.$setPristine();
            $scope.ContactForm.$setUntouched();
        });
    };

    $scope.addSkill = function(new_skill, contact) {
        var data = $httpParamSerializer({
            name: new_skill.name,
            level: new_skill.level,
            contacts: [ contact.id ],
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.post('/api/skills/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.getContact(contact.id);
            $scope.new_skill = undefined;
            $scope.SkillForm.$setPristine();
            $scope.SkillForm.$setUntouched();
        });
    };

    /**
     * Updates or removes a skill from contact.
     *
     * Updates skill name and/or skill level for a specified contact.
     * In case remove parameter is set to true removes skill from the contact. 
     * 
     * @param   {Object}    skill           Skill to be updated.
     * @param   {number}    skill.id        Skill identification. Private key.
     * @param   {string}    skill.name      Skill name.
     * @param   {number}    skill.level     Skill level.
     * @param   {Object}    contact         Conact to have the skill updated.
     * @param   {number}    contact.id      Contact identification. Private key.
     * @param   {type}      [remove=false]  Switches standart update behavior. If set to true removes skill from contact.
     * 
     * @return  {Object}                    Updated skill.
     */
    $scope.updateSkill = function(skill, contact, remove=false) {
        var data;
        if (remove) {
            data = $httpParamSerializer({
                contacts: [ contact.id ],
            });
        } else { 
            data = $httpParamSerializer({
                name: skill.name,
                level: skill.level,
                contacts: [ contact.id ],
            });
        }
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.put('/api/skills/' + skill.id + '/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.getContact(contact.id);
            $scope.SkillForm.$setPristine();
            $scope.SkillForm.$setUntouched();
        });
    };
});

// Global scope variables
app.run(function($rootScope) {
    $rootScope.icon_add_user = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARZSURBVGhD7ZlZqFZVFMdvVpalGNlEhZkWNhA0EiFFYUT0EKQ5RKQgJT00QBFEJRFRBFI0UJYZhaL0UgSBikQTPRSFWRENVNAgNNhENNhkvx/cBYuPc+53zvnynO/h/uH3su/e+6x9915rr7W/kXGNa/g0GS6FJ+AV+ADegufhVjgRhlqT4Bb4EXb14UU4HYZOs+B9KDK6jH/gZtgDhkInwfeQjfwOVsNSuBAuAY1+DXI/eQQ618HwCYRRf8NdoJ+U6Wzo3b3roVPp0GHMTrgYqmgKvAQx9g+YCZ3oBHAHwpjroI4OgM8gxq+HTrQSwoitMAHqaj7EHO7oVGhdH0MYcaUNDWTE2g4xz2XQqvaF+LgcCU2V/exuG9qUjhkf/wuaHKvQ7RBzPWVDmzoe4uOe7UF0G8RcT9vQpg6C+LgcBk31KMQ8D9rQtrKTXm5DQ+UL9Sob2lZ2UrPcJjofYo5/YZCg0VhnQRghC6GO9oN3IMZvhs60CcKQX+FMqKK9QceOsWbCVcfuFh0NP0EY9Dssh72gTMfAyxBj5D7oXHPBBWTDPoQVcB4cB6eBt7a7YLjOfd3VsoWbXB4B7mAr0uBvIRtYhXUwEUIa7b1iZvwbRD8DwdfwLCyB3ZaTGX3ehmxkP8wITEkOBOuaJ+FPKOrbyw9wI5gq/S/yItwIRR+rys/QW2FWxag3AwbSudB7nIw+r4Nl7Rw4CvYBK0br+gWwBvyP5nEZ/cvXFh8nDgWPnkdOX3wALKNz/29AH2ykiyCfYdFpT4Yq2h9y+BWj3zIYK+IpCzJrIf0mxn4JLraWzoAcebw/6l6GHskdEHNYKVpx1pFFmSVyzPEqVH6RmQZfQAz2aJ0KdaVjxxzuRNGj3Wz4dJRtNhToCoh5xKNbSY9DDHJXTFPqajoYsWIej1ORfGaKPi62TBsg+ulffeV/XmeOQVdDE+nIMYfPqXtCkaouxOwi/2P6npC1EJ3fg6ZVYU5PvP3LVHUhyifY6HuHDWXyJs1Rqur7VZEMDjFPfv/VcMNosAii3y+jbRl3InQTRN9nbCjTPIiOPlI3zX28T2IeOQRCn0P+Wz/yO5hRM9rfsKFM90LRBHV1OMQ8kvOsQRZyAUT7RzaUaQtExxtsaCh3Ml9kuSJ8F7zxA1OX6OeY/DfxkTyUw/CY1ao/1ETHxTYMILPYmMu0o0x1nP1OiL5jvsToTPeMcqwNA8hUPD5q7lSmOgtxN6PvtTa0IX8ziY+appTVFlUXcg5EP4+gF24r0vCctpsAFqnKQrxM34Topy+3Koui+Lj/RcN7r8xmHxvlfhsK9BDkebxfWpWVXT7X1vxGnqoy1c+LkIehE1l09RZmJoD5xi6SBZ2XXh5nyM13Uus6Bb6CbJQJoLmTkdI0xcvO3fK3ybyLgXWI5UXn8rbXmF4D+6FPrIJOd6JXVnYWRaYXRUZnXMAL4G4Otawn/PHnOfAhw8W5Y/rPNdDaPTGucZVqZOQ/FRoQ53gVmukAAAAASUVORK5CYII=";
    $rootScope.icon_edit = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHfSURBVGhD7Zk7Sx1RFEavWIiPQOxNwEa7EKtoRP+H6UQSLYyNpBTBXlDsJWWwzy+I2mhlLBNIMJVWmoCKoq6PuGFzObmoA5kt7AULZs7cM+yP8xg4t5EkSZI8kOe4gJ9xCzfwLXbio+EDnuF1wV84hqFpwzUsBfCeY9gwpRA/cRLHcRH9KB1guGlWCrGNT9HzCn2YKQxDKcQVvsQSGhn73Sc1RKDVmtC06sdmXqP95osa6qYU4htqNOy+FEZrxp5ra66VUogd1JrQvP9XmF78gfZM35naaBXCKIUZQn0Yre0Un2Et3CWE0RzGX8t5rIX7hDCaw5irWAsPCSH0/Dv6fnqP3vffqRJiF32/DFGFDIG+X4aoQoZA3y9DVCFDoO+XIaqQIdD3qy2EWEFfzAW+wFaEC9GNl+gLkn/wHZYIF0L4E4ySS+gJGULMoRWko5hpPHRt0kYmbAjxEa2oZTWADgD20dp/o9ZM2BBiD62wN2q4pQ+P0J5pA7BrGSpEF/qFPoieGfTFm6FCiGG04k6wHQdwAjXNNtEHkOFCiPdoBepw7NjdlwwZQqxjqeBmNf107hQyhPA7k6lF/RW1m2nERlEfzbD0oP7uUtEamVkcQW0Aj4oOfPL3MkmSJAyNxg1x2mXbXV7r+QAAAABJRU5ErkJggg==";
    $rootScope.icon_save = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEwSURBVGhD7ZkxjsIwEEUjigXKvQAFPRWn4AA0dFxy9wC0e5ItViDokID5kkcaWUk2TiYDEv9JTwI7xn4FLqAihBDyiszFdaAf4iisxHugX+JUdCc6BH6LM9EVG3IT/zIvos5f01id+gw8pjGINXZOdY+xIThAzk7U+QMGGtBn4AIDCazR8V/zGrrGRIbsRRzePusWExmCz8IXfZQYr5BP4wQDiTwENMUMupq9QpqoCwF1MThLb54VAhBjb8WwkLP4UyjW6Po8BGBPnQ8LGSpDuvBfCK7SrZP2WlbCQsaGITkMcSIkxG7iZdseDAFvF7IRlz3F2i57hIQM2SRiD4aUwJASGFIAQ0pgSAEMKcFukv+Ijfc6d0pjfcTaLnu4hTxbhoDov97axFkIIYS8ElX1ALJPbVp9kizNAAAAAElFTkSuQmCC";
    $rootScope.icon_trash = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFwSURBVGhD7ZmtSgVRFIVHBDEIahMUX0AFg8EgWHwEQRCsPoAWq8Fg1SCCVYuCJvEHk8VkEGwWX8AsFl0L9oaDHPHOZZ87w2V98JXFMPssmDn3cqYSQggBpuEBvIH3Ge/gMZyFrWUSfsDvDvyE87CV7MHcov/yDLaSS+iLPIWbGQ+hX/MMe8oAHO/AW+iL3Lbst2vQr3m17D8HYQij0Ic34RwMQUWCDCvi78gu9JufWxZtbkbYO+LsQB/CXakEvZihInVotMgYXDGXGCR4TocZGAvQ8wkGRqNFuHjP3xkkeE75h9J5hJ6vMzBUpA4qYqpINCpiqkg0KmKqSDQqYqpINCpitr7IIuSZL31hkOA5nWJgXEPPVxkYjRaJREXq0DdFeDDtQx4YFOAE+gye3BdhGfoQegRznw66dR9+Qb//BiwCj06fYFqmlG8wPT4Kh1sot9jc8Cj5WzQDizME+ShcwNwHz269gltwBAohRF9SVT/YcCJDemJ9EwAAAABJRU5ErkJggg==";
});
