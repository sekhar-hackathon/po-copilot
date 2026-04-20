import React, { useState } from 'react';
import api from '../services/api';

const ReportGenerator = () => {
    const [reportData, setReportData] = useState({});
    const [reportPaths, setReportPaths] = useState(null);

    const handleGenerateReport = async () => {
        try {
            const response = await api.post('/generate-report', reportData);
            setReportPaths(response.data);
        } catch (error) {
            console.error('Error generating report:', error);
        }
    };

    return (
        <div>
            <h2>Generate Monthly Reliability Report</h2>
            <button onClick={handleGenerateReport}>Generate Report</button>
            {reportPaths && (
                <div>
                    <a href={reportPaths.pdf} download>Download PDF</a>
                    <a href={reportPaths.excel} download>Download Excel</a>
                </div>
            )}
        </div>
    );
};

export default ReportGenerator;
