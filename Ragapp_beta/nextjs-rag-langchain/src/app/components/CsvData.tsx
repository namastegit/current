// // // components/CsvData.tsx
// "use client"

// // components/CsvData.tsx
// import React, { useState, useEffect } from 'react';

// const CsvData: React.FC = () => {
//   const [data, setData] = useState<any[]>([]);

//   useEffect(() => {
//     fetchData();
//   }, []);

//   const fetchData = async () => {
//     try {
//       const response = await fetch('/data.csv'); // Access the CSV file directly from the public folder
//       if (response.ok) {
//         const csvData = await response.text();
//         const parsedData = parseCsv(csvData);
//         setData(parsedData);
//       } else {
//         console.error('Failed to fetch CSV data:', response.statusText);
//       }
//     } catch (error) {
//       console.error('Error fetching CSV data:', error);
//     }
//   };

//   const parseCsv = (csvData: string) => {
//     const lines = csvData.split('\n');
//     const parsedData: any[] = [];

//     // Iterate through each line of the CSV data
//     for (let i = 0; i < lines.length; i++) {
//       const line = lines[i].trim(); // Remove leading/trailing whitespace
//       if (line.length === 0) continue; // Skip empty lines

//       // Remove surrounding square brackets
//       const lineWithoutBrackets = line.replace(/^\[|\]$/g, '');

//       // Split the line by comma, handling escaped double quotes
//       const row = lineWithoutBrackets.split(/,(?=(?:[^"]|"[^"]*")*$)/);

//       // Remove surrounding double quotes from each field
//       const cleanedRow = row.map(field => field.replace(/^"|"$/g, ''));

//       // Add the cleaned row to the parsed data array
//       parsedData.push(cleanedRow);
//     }

//     return parsedData;
//   };

//   return (
//     <div>
//       <h2>CSV Data</h2>
//       <ul>
//         {data.map((row, index) => (
//           <li key={index}>{JSON.stringify(row)}</li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default CsvData;


// // import React, { useState, useEffect } from 'react';

// // const CsvData: React.FC = () => {
// //   const [data, setData] = useState<any[]>([]);

// //   useEffect(() => {
// //     fetchData();
// //   }, []);

// //   const fetchData = async () => {
// //     try {
// //       const response = await fetch('/data.csv'); // Access the CSV file directly from the public folder
// //       if (response.ok) {
// //         const csvData = await response.text();
// //         const parsedData = parseCsv(csvData);
// //         setData(parsedData);
// //       } else {
// //         console.error('Failed to fetch CSV data:', response.statusText);
// //       }
// //     } catch (error) {
// //       console.error('Error fetching CSV data:', error);
// //     }
// //   };

// //   const parseCsv = (csvData: string) => {
// //     // Implement CSV parsing logic here
// //     // This is just a basic example, you might need to use a library like 'csv-parser'
// //     const lines = csvData.split('\n');
// //     const parsedData: any[] = lines.map(line => line.split(','));
// //     return parsedData;
// //   };

// //   return (
// //     <div>
// //       <h2>CSV Data</h2>
// //       <ul>
// //         {data.map((row, index) => (
// //           <li key={index}>{JSON.stringify(row)}</li>
// //         ))}
// //       </ul>
// //     </div>
// //   );
// // };

// // export default CsvData;
