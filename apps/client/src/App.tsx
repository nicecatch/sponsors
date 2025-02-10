"use client";
import './App.css';
import React, { useEffect, useState } from "react";
import { Table, Input, Card } from "antd";
import { ColumnType } from "antd/es/table";
import { debounce } from "lodash";

export default function DataTable() {
  const [data, setData] = useState<any[]>([]);
  const [filters, setFilters] = useState<{ [key: string]: string }>({});

  // Fetch data from Flask API
  async function fetchData(filters = {}) {
    const response = await fetch("http://127.0.0.1:8000/filter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(Object.entries(filters)),
    });
    const result = await response.json();
    setData(result);
  }

  useEffect(() => {
    fetchData(); // Load data initially
  }, []);

  // Handle filter input change with debounce to avoid excessive requests
  const handleFilterChange = debounce((column: string, value: string) => {
    const newFilters = { ...filters, [column]: value };
    if (value === "") delete newFilters[column]; // Remove empty filters
    setFilters(newFilters);
    fetchData(newFilters);
  }, 300); // Debounce delay of 300ms

  // Ant Design table column configuration
  const columns: ColumnType<any>[] =
    data.length > 0
      ? Object.keys(data[0]).map((key) => ({
          title: (
            <div>
              <span className="font-bold">{key}</span>
              <Input
                placeholder={`Filter ${key}`}
                onChange={(e) => handleFilterChange(key, e.target.value)}
                style={{ marginTop: 5 }}
              />
            </div>
          ),
          dataIndex: key,
          key: key,
          render: (text: string) => <span>{text}</span>,
        }))
      : [];

  return (
    <Card className="p-4 max-w-4xl mx-auto mt-10">
      <h1 className="text-xl font-bold mb-4">Data Table with Filters</h1>
      <Table
        columns={columns}
        dataSource={data}
        rowKey={(record) => record.id} // Assuming each record has a unique "id"
        pagination={false} // Disable pagination to keep it simple
      />
    </Card>
  );
}
