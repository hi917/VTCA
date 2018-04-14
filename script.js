/**
 * Load required modules
 */
var $ = require('jquery');
var FileSaver = require('file-saver');

$(document).ready(function() {
	/**
	 * Checks to ensure user entered valid term input
	 */
	function validTerm(term) {
		if (term === '' || term.length != 6) {
			alert('Invalid term input. Format is YYYYMM. For example, 201801 for Spring 2018.');
			return false;
		}
		let month = term.substring(term.length-2);
		if (month !== '01' && month !== '06' && month !== '07' && month !== '09') {
			alert('Invalid month for term.\nSpring: 01, Summer I: 06, Summer II: 07, Fall: 09');
			return false;
		}
		let year = term.substring(0, term.length-2);
		let currentYear = (new Date).getFullYear();
		if (year < currentYear) {
			alert('Invalid year for term.');
			return false;
		}
		return true;
	}

	/**
	 * Adds course to listening table with information from course form
	 */
	$('.button_div').on('click', ':submit', function(event) {
		event.preventDefault();
		let courseNum = $('.listening_table tr').length;
		let term = $('.term_div').find('input').val();
		if (!validTerm(term)) {
			return;
		}
		let cle = $('.cle_div').find('select').val();
		let courseCRN = $('.crn_div').find('input').val();
		let courseSubject = $('.subject_div').find('select').val();
		let courseNumber = $('.cn_div').find('input').val();
		let removeButton = '<button>Remove</button>';
		let course = 
			'<tr class="course"><td>' + courseNum +
			'</td><td>' + courseCRN + 
			'</td><td>' + (courseSubject + "-" + courseNumber) + 
			'</td><td>' + cle +
			'</td><td>' + term + 
			'</td><td>' + removeButton + 
			'</td></tr>';
		$('.listening_table').append(course);
	});

	/**
	 * Remove course from listening table
	 */
	$('.listening_table').on('click', ':button', function() {
		$(this).closest('tr').remove();
		// Update each listening table row's # cell
		let rowNum = 0;
		$('.listening_table tr').each(function() {
			$(this).find('td:eq(0)').text(rowNum++);
		});
	});

	/**
	 * Extracts information from listening table and creates a .txt file with it
	 */
	$('.save_file_div').on('click', ':button', function () {
		let text = '\n';
		let row = 0;
		$('.listening_table>tbody>tr').each(function() {
			if (row != 0) {
				let courseCRN = $(this).find('td:eq(1)').text();
				console.log(courseCRN);
				let subject_number = $(this).find('td:eq(2)').text().split('-');
				let courseSubject = subject_number[0];
				let courseNumber = subject_number[1];
				let cle = $(this).find('td:eq(3)').text();
				let term = $(this).find('td:eq(4)').text();
				let course = courseCRN + '|' + courseSubject + '|' + courseNumber + '|' + cle 
					+ '|' + term + '|true\n';
				console.log(course);
				text += course;
			}
			row++;
		});
		let blob = new Blob(['', text], {type:'text/plain;charset=utf-8'});
		FileSaver.saveAs(blob, 'listening_list.txt');
	});
});