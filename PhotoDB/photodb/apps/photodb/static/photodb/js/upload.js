upload_form = new Vue({
    el: '#upload_form',
    delimiters: ['[[', ']]'],
    data: {
        urls: {
            'photo': window.location.origin +'/api/v1/photos/',
        },
        cookie: _get_cookie('csrftoken'),
        photos: [],
        uploaded: [],
        year: '',
        month: '',
        day: '',
        tags: [],
        new_tag: '',
        errors: [],
    },
    methods: {
        reset: function(){
            this.uploaded = [];
            this.errors = [];
        },
        removeTag: function(tag){
            this.tags = this.tags.filter(el => el !== tag);
        },
        addTag: function(){
            this.tags.push(this.new_tag)
            this.new_tag = '';
        },
        processPhotos: function(event){
            this.photos = event.target.files
        },
        submit: function(){
            this.reset()
            if(this.tags.length > 0){
                let promises = Tag.create_tags(this.tags);
                axios.all(promises)
                .then( response => {
                    this.uploadPhotos();
                })
                .catch( error => {
                    this.uploadPhotos();
                })
            }else{
                this.uploadPhotos();
            }
        },
        tagError: function(error){
            console.log(error)
        },
        uploadPhotos: function(){
            Array.from(this.photos).forEach( photo => {
                this.uploadSinglePhoto(photo)
            })
        },
        uploadSinglePhoto: function(photo){
            data = new FormData();
            data.append('image', photo);
            data.append('year', this.year);
            data.append('month', this.month);
            data.append('day', this.day);
            this.tags.forEach(function(tag){
                data.append('tags', tag)
            })
            axios({
                method: 'post',
                url: this.urls['photo'],
                data: data,
                headers: {
                    'X-CSRFToken': this.cookie
                }
            })
            .then( response => {
                this.uploaded.push(response.data);
            })
            .catch( error => {
                let msg = error.response.data[0]
                console.log(msg)
                this.errors.push(msg)
            })
        }
    }
})