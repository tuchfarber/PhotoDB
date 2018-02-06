PHOTOS_API_URL = window.location.origin + '/api/v1/photos/';
TAG_API_URL = window.location.origin + '/api/v1/tags/'

function _get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function _bulk_call(arr, f){
    let promises = [];
    arr.forEach(item => {
        promises.push(f(item))
    })
    return promises;
}

class Photo{

    constructor(photo) {
        this.id = photo.id;
        this.tags = photo.tags;
        this.year = photo.year;
        this.month = photo.month;
        this.day = photo.day;
    }

    get data() {
        let data = {
            'tags': this.tags,
            'year': this.year,
            'month': this.month,
            'day': this.day
        }
        return data;
    }

    static search(query){
        return axios.get(PHOTOS_API_URL + '?q=' + query)
    }
    static create_photo(photo) {

    }
    static create_photos(photos) {

    }
    static read_photo(photo) {

    }
    static read_photos(photos) {
        
    }
    static update_photo(photo) {
        return axios({
            method: 'patch',
            url: PHOTOS_API_URL + photo.id + '/',
            data: photo.data,
            headers: {
                'X-CSRFToken': _get_cookie('csrftoken')
            }
        })
    }
    static update_photos(photos) {
        return _bulk_call(photos, this.update_photo)
    }
    static delete_photo(photo) {
        return axios({
            method: 'delete',
            url: PHOTOS_API_URL + photo.id + '/',
            headers: {
                'X-CSRFToken': _get_cookie('csrftoken')
            }
        })
    }
    static delete_photos(photos) {
        return _bulk_call(photos, this.delete_photo)
    }
}


class Tag{
    static create_tag(name) {
        return axios({
            method: 'post',
            url: TAG_API_URL,
            data: {'name': name},
            headers: {
                'X-CSRFToken': _get_cookie('csrftoken')
            }
        })
    }
    static create_tags(names) {
        return _bulk_call(names, this.create_tag)
    }
    static read_tag(name) {

    }
    static read_tags(names) {

    }
    static update_tag(name) {

    }
    static update_tags(names) {

    }
    static delete_tag(name) {

    }
    static delete_tags(names) {

    }
}