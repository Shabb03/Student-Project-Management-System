var express = require('express');
var router = express.Router();

//---AUTHENTICATION----------------------------------------------------------------------------------------------------------

router.get('/', function(req, res, next) {
  res.render('login', { title: 'Login' });
});
router.get('/register', function(req, res, next){
  res.render('register', { title: 'Sign Up' })
});
router.get('/profile', function(req, res, next){
  res.render('profile', { title: 'Profile' })
});
router.get('/waiting', function(req, res, next){
  res.render('waiting', { title: 'Waiting' })
});


//---ADMIN-------------------------------------------------------------------------------------------------------------------

router.get('/adminpage', function(req, res, next){
  res.render('adminpage', { title: 'Homepage' })
});
router.get('/deadline', function(req, res, next){
  res.render('deadline', { title: 'Deadlines' })
});
router.get('/newprofessors', function(req, res, next){
  res.render('newprofessors', { title: 'New Professors' })
});
router.get('/studentslist', function(req, res, next){
  res.render('studentslist', { title: 'Students' })
});
router.get('/assignstudent', function(req, res, next){
  res.render('assignstudent', { title: 'Assign Students' })
});
router.get('/professorslist', function(req, res, next){
  res.render('professorslist', { title: 'Professors' })
});
router.get('/professortimelist', function(req, res, next){
  res.render('professortimelist', { title: 'Timetable' })
});
router.get('/professortime', function(req, res, next){
  res.render('professortime', { title: 'Time Slots' })
});
router.get('/venues', function(req, res, next){
  res.render('venues', { title: 'Venues' })
});
router.get('/timetable', function(req, res, next){
  res.render('timetable', { title: 'Generate Timetable' })
});
router.get('/demonstration', function(req, res, next){
  res.render('demonstration', { title: 'Demonstration Timetable' })
});
router.get('/reset', function(req, res, next){
  res.render('reset', { title: 'Reset' })
});


//---STUDENT-----------------------------------------------------------------------------------------------------------------

router.get('/studentpage', function(req, res, next){ 
  res.render('studentpage', { title: 'Homepage' });
});
router.get('/proposal', function(req, res, next){ 
  res.render('proposal', { title: 'Proposal' });
});
router.get('/submitproposal', function(req, res, next){ 
  res.render('submitproposal', { title: 'Submit Proposal' });
});
router.get('/files', function(req, res, next){ 
  res.render('files', { title: 'Files' });
});
router.get('/meeting', function(req, res, next){ 
  res.render('meeting', { title: 'Meeting' });
});
router.get('/meetinghistory', function(req, res, next){ 
  res.render('meetinghistory', { title: 'Meeting History' });
});
router.get('/editdetails', function(req, res, next){ 
  res.render('editdetails', { title: 'Edit Details' });
});


//---PROFESSOR---------------------------------------------------------------------------------------------------------------

router.get('/professorpage', function(req, res, next){ 
  res.render('professorpage', { title: 'Homepage' });
});
router.get('/proposalslist', function(req, res, next){ 
  res.render('proposalslist', { title: 'Proposals' });
});
router.get('/studentproposal', function(req, res, next){ 
  res.render('studentproposal', { title: 'Student Proposal' });
});
router.get('/addtimetable', function(req, res, next){ 
  res.render('addtimetable', { title: 'Timetable' });
});
router.get('/profmeeting', function(req, res, next){ 
  res.render('profmeeting', { title: 'Meeting' });
});
router.get('/profmeetinghistory', function(req, res, next){ 
  res.render('profmeetinghistory', { title: 'Meeting History' });
});
router.get('/meetingform', function(req, res, next){ 
  res.render('meetingform', { title: 'Supervision Form' });
});
router.get('/projects', function(req, res, next){ 
  res.render('projects', { title: 'Projects' });
});
router.get('/studentproject', function(req, res, next){ 
  res.render('studentproject', { title: 'Student Project' });
});
router.get('/proftimetable', function(req, res, next){ 
  res.render('proftimetable', { title: 'Demonstration Timetable' });
});


//---MISCELLANEOUS-----------------------------------------------------------------------------------------------------------

router.get('*', function(req, res, next){ 
  res.render('error404', { title: 'Page Not Found' });
}); 

module.exports = router;