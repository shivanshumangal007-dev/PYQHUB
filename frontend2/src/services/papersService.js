import apiClient from "./apiClient";
import { mockPapers } from "../data/mockPapers";

const normalizePaper = (paper) => {
	return {
		id: paper.id,
		title: paper.subject?.name || paper.title || "Untitled",
		semester: Number(paper.semester || paper.subject?.semester.number || 1),
		year: Number(paper.year || new Date().getFullYear()),
		examType: paper.exam_type || paper.examType || "Regular",
		pdf: paper.pdf || "#",
	};
};

export const getSubjectsBySemester = async (semester) => {
	try {
		const response = await apiClient.get(`/subject/${semester}`);
		// const payload = Array.isArray(response.data.subjects) ? response.data.subjects : [];
		
		const result = response.data.subjects.map((subject) => ({
			id: subject.id,
			name: subject.name,
		}));
		return result;
	} catch {
		return [];
	}
};

export const getPapers = async ({ semester, exam, subjectIds }) => {
	try {
        console.log("Fetching papers with params:", { semester, exam, subjectIds });
		const response = await apiClient.post("/get-papers", {
			semester,
			exam,
			subject: subjectIds,
		});
		const payload = Array.isArray(response.data?.papers)
			? response.data.papers
			: [];
		
		return payload.map(normalizePaper);
	} catch {
		return mockPapers;
	} 
};
