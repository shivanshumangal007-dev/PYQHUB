import { useState } from "react";
import api from "../../services/apiClient.js";

const UploadPanel = ({ logoutHandler }) => {
	const [title, setTitle] = useState("");
	const [semester, setSemester] = useState("S5");
	const [examType, setExamType] = useState("End Sem");
	const [year, setYear] = useState("");
	const [file, setFile] = useState(null);
	const [subjectId, setSubjectId] = useState(""); // ⚠️ important

	const handleSubmit = async () => {
		try {
			const formData = new FormData();

			formData.append("title", title);
			formData.append("subject_id", subjectId); // 🔥 backend expects this
			formData.append("year", year);
			formData.append("examType", examType.toLowerCase().replace(" ", ""));
			formData.append("semester", semester.replace("S", ""));
			formData.append("file", file);

			const token = localStorage.getItem("ACCESS_TOKEN");

			await api.post("/add-paper", formData, {
				headers: {
					Authorization: `Bearer ${token}`,
					"Content-Type": "multipart/form-data",
				},
			});

			alert("Upload successful 🚀");
		} catch (err) {
			console.log(err);
			alert("Upload failed ❌");
		}
	};

	return (
		<section className='upload-page'>
			<div className='upload-shell'>
				<div className='upload-head'>
					<div>
						<p className='upload-eyebrow'>Upload Sector</p>
						<h1>Submit and manage your paper uploads.</h1>
						<p>
							This section is ready from frontend side. Backend
							integration can be attached without changing this page
							structure.
						</p>
					</div>
					<span className='preview-badge'>
						<button onClick={logoutHandler}>logout</button>
					</span>
				</div>

				<div className='upload-grid'>
					<div className='upload-card'>
						<h3>Paper Metadata</h3>
						<div className='upload-form-grid'>
							<label>
								<span>Subject ID</span>
								<input
									type='number'
									placeholder='Enter subject ID'
									onChange={(e) => setSubjectId(e.target.value)}
								/>
							</label>

							<label>
								<span>Title</span>
								<input
									type='text'
									placeholder='e.g. Computer Networks Midsem'
									onChange={(e) => setTitle(e.target.value)}
								/>
							</label>

							<label>
								<span>Semester</span>
								<select
									value={semester}
									onChange={(e) => setSemester(e.target.value)}
								>
									<option>S1</option>
									<option>S2</option>
									<option>S3</option>
									<option>S4</option>
									<option>S5</option>
									<option>S6</option>
									<option>S7</option>
									<option>S8</option>
								</select>
							</label>

							<label>
								<span>Examination Type</span>
								<select
									value={examType}
									onChange={(e) => setExamType(e.target.value)}
								>
									<option>Mid Sem</option>
									<option>End Sem</option>
									<option>Regular</option>
									<option>Supplementary</option>
								</select>
							</label>

							<label>
								<span>Year</span>
								<input
									type='number'
									min='2000'
									max='2100'
									placeholder='2026'
									onChange={(e) => setYear(e.target.value)}
								/>
							</label>
						</div>
					</div>

					<div className='upload-card'>
						<h3>File Upload</h3>
						<div className='drop-zone'>
							<p>Drag and drop PDF here</p>
							<span>or click to select file</span>
							<input
								type='file'
								accept='application/pdf'
								onChange={(e) => setFile(e.target.files[0])}
							/>
						</div>
						<div className='upload-actions'>
							<button
								type='button'
								className='primary-action'
								onClick={handleSubmit}
							>
								Submit Upload
							</button>
							<button type='button' className='secondary-action'>
								Save Draft
							</button>
						</div>
						<p className='muted-text'>
							Buttons are UI placeholders until backend endpoint is
							connected.
						</p>
					</div>
				</div>
			</div>
		</section>
	);
};

export default UploadPanel;
