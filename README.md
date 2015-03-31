# geno-browser

The goal of this project is to do a remake of the popular [UCSC Genome Browser](http://genome.ucsc.edu/)

We will focus on adding more features that cater towards non-eukaryotic organisms.

# API
## Users
#### GET /api/users/(int:user_id)

Response: {  
    user_name: (user_name),  
    user_id: (user_id),  
    email: (email)  
}  

#### POST /api/users

Request fields: {  
    {  
        user_name:(username),  
        email:(email)  
    }  
  
Response: {  
    user_id: (user_id)  
}  

#### PUT /api/users/(int:user_id)

Request fields: {  
    user_name: (new_user_name), // optional  
    email: (new_email)          // optional  
}  
  
Response: {  
    user_name: (user_name),  
    user_id: (user_id),  
    email: (email)  
}  

#### DELETE /api/users/(int:user_id)

Response: {}  

## Views
#### GET /api/views/(int:view_id)

Required Request Headers: X-Userid

Response: {  
    view_id: (view_id),  
    view_name: (view_name),  
    view_tracks: [  
        {  
            track_id: (track_id),  
            type:     (track_type),  
            sticky:   (is_sticky),  
            hidden:   (is_hidden),  
            tooltips: [  
                {  
                    pos: (int:tooltip position),  
                    body: (innert text)  
                },  
                ...  
            ],  
            y-scale: {  
                min: (int:min),  
                max: (int:max)  
            },  
            display: (display type)  
        },  
        ...  
    ],  
    comments:[  
        {  
            user_id: (user_id),  
            body:    (text)  
        },  
        ...  
    ]  
}  
  
#### PUT /api/views/(int:view_id)  

Required Request Headers: X-Userid

Request Data: same as response from GET

Response: {  
    view_id: (view_id)  
}  
  
#### POST /api/views/(int:view_id)

Required Request Headers: X-Userid

Request Data: {  
    track_ids: [(track_id), ... ]  
}  

#### DELETE /api/views/(int:view_id)

Required Request Headers: X-Userid

Response: {}  

## Tracks
#### GET /api/tracks

Required Request Headers: X-Userid

Response: {  
    tracks: [  
        {  
            track_id   : (track_id),  
            track_name : (track_name),  
            user_id    : (user_id),  
            data_type  : (data_type),  
            data_id    : (data_id),  
            file_name  : (file_name)  
        },  
        ...  
    ]  
}  

#### GET /api/tracks/(int:track_id)

Required Request Headers: X-Userid

Response: {  
    track_id   : (track_id),  
    track_name : (track_name),  
    user_id    : (user_id),  
    data_type  : (data_type),  
    data_id    : (data_id),  
    file_name  : (file_name)  
}  

#### POST /api/tracks

Required Request Headers: X-Userid

Request Data: {  
    track_name : (track_name),  
    user_id    : (user_id),  
    data_type  : (data_type),  
    data_id    : (data_id),  
    file_name  : (file_name)  
}  
  
Response: {  
    track_id: (track_id)  
}  

#### PUT /api/tracks/(int:track_id)

Required Request Headers: X-Userid  

Request Data: {  
    track_name : (track_name),  
    user_id    : (user_id),  
    data_type  : (data_type),  
    data_id    : (data_id),  
    file_name  : (file_name)  
}  

Response: {  
    track_id   : (track_id),  
    track_name : (track_name),  
    user_id    : (user_id),  
    data_type  : (data_type),  
    data_id    : (data_id),  
    file_name  : (file_name)  
}  

## DELETE /api/tracks/(int:track_id)

Required Request Headers: X-Userid

Response: {}  
