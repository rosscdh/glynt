/**
 * LawPal Data object used by AngularJS
 */
var LawPal = {
	/**
	 * Primary list of the checklist items
	 */
	"checklist_data": function () {
		return [{
			"category": "Qualification to do business",
			"data": "{}",
			"date_created": "2013-08-28T12:54:14.394268",
			"date_due": null,
			"date_modified": "2013-08-28T12:54:14.394333",
			"description": "",
			"id": 1,
			"is_deleted": false,
			"name": "File Form DE-1 (State employer identification number for the Company in California)",
			"project": 1,
			"slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295",
			"sort_position": 21,
			"sort_position_by_cat": 1,
			"status": 0
		}, {
			"category": "Intellectual Property",
			"data": "{}",
			"date_created": "2013-08-28T12:54:14.394419",
			"date_due": null,
			"date_modified": "2013-08-28T12:54:14.394440",
			"description": "",
			"id": 2,
			"is_deleted": false,
			"name": "IP created by non-Founders",
			"project": 1,
			"slug": "5f08359d452e571f64f5442ad845f365d5d989ca",
			"sort_position": 33,
			"sort_position_by_cat": 1,
			"status": 0
		}];
	},
	/**
	 * Feedback requests are requests that are associated
	 * with an item that applies to the currentuser
	 */
	"feedback_requests": function () {
		return {
			"1dfefcfe4f86d49254cd2ddd57331b17deff2295": [{
				"todo_slug": "1dfefcfe4f86d49254cd2ddd57331b17deff2295"
			}]
		}
	},
	"is_lawyer": true,
	"is_customer": false,
	"checklist_categories": function () {
		return [{
			"label": "General",
			"slug": "general"
		}, {
			"label": "Qualification to do business",
			"slug": "qualification-to-do-business"
		}, {
			"label": "Founders Documents",
			"slug": "founders-documents"
		}, {
			"label": "Option Plan",
			"slug": "option-plan"
		}, {
			"label": "Option Holders",
			"slug": "option-holders"
		}, {
			"label": "Option Holders - International",
			"slug": "option-holders-international"
		}, {
			"label": "Directors &amp; Officers",
			"slug": "directors-officers"
		}, {
			"label": "Employment Documents",
			"slug": "employment-documents"
		}, {
			"label": "Consultant Documents",
			"slug": "consultant-documents"
		}, {
			"label": "Intellectual Property",
			"slug": "intellectual-property"
		}, {
			"label": "Miscellaneous",
			"slug": "miscellaneous"
		}, {
			"label": "",
			"slug": ""
		}];
	},
	"getEndpoint": function () {
		var urls = {
			"checklist": {
				"item": {
					"view": "/todo/:project_uuid/:slug/",
					"create": "/todo/:project_uuid/create/?category=:categoryLabel",
					"form": "/todo/:project_uuid/:slug/edit/"
				}
			}
		};

		return function (path) {
			var url = urls;
			if (angular.isArray(path)) {
				for (var i = 0; i < path.length; i++) {
					url = url[path[i]];
				}
				if (angular.isString(url))
					return url;
				else
					return null;
			}
		}
	}
};