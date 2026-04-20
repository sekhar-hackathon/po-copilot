import React, { useState } from 'react';
import api from '../services/api';

const ReportGenerator = () => {
    const [format, setFormat] = useState('pdf');
    const [data, setData] = useState([]);

    const handleGenerateReport = async () => {
        try {
            const response = await api.post('/generate-report', { data, format });
            alert(`Report generated: ${response.data.file_path}`);
        } catch (error) {
            console.error('Error generating report:', error);
            alert('Failed to generate report');
        }
    };

    return (
        <div>
            <h2>Generate Monthly Reliability Report</h2>
            <select value={format} onChange={(e) => setFormat(e.target.value)}>
                <option value="pdf">PDF</option>
                <option value="excel">Excel</option>
            </select>
            <button onClick={handleGenerateReport}>Generate Report</button>
        </div>
    );
};

export default ReportGenerator;
