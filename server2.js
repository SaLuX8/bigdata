const express = require('express')
const bodyParser= require('body-parser')
const MongoClient = require('mongodb').MongoClient
const app = express()

app.use(bodyParser.urlencoded({extended: true}))

var db, result

MongoClient.connect('mongodb://192.168.1.20:27017', { useUnifiedTopology: true }, (err, client) => {
  if (err) return console.log(err)
  db = client.db('weatherdb')
  app.listen(3000, () => {
    console.log('Palvelu käynnistetty porttiin 3000')
  })
})

app.get('/', (req, res) => {
db.collection('weatherdata').aggregate([
        {$group:{_id:"$_id", timestamp:{$first:"$timestamp"}, temp:{$first:"$temp"},visibility:{$first:"$visibility"},windspeed:{$first:"$windspeed"}}}
        ]).toArray((err, result) => {
        if (err) return console.log(err)
        res.render('index2.ejs', {weatherdata: result})
    })
})

app.get('/reload', (req, res) => {
    result = []
    db.collection('weatherdata').aggregate([
        {$group: {_id:"$_id", minTemp:{$min:"$temp"},maxTemp:{$max:"$temp"},avgTemp:{$avg:"$temp"}}}
    ]).toArray((err, result) => {
        if (err) return console.log(err)
        res.json(result)
    })
})
