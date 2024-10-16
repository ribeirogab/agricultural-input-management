CREATE TABLE supplier (
    id VARCHAR2(36) PRIMARY KEY,
    name VARCHAR2(255) NOT NULL,
    email VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL  -- Field to store soft delete information
);

CREATE TABLE supply (
    id VARCHAR2(36) PRIMARY KEY,
    name VARCHAR2(255) NOT NULL,
    quantity NUMBER NOT NULL,
    type VARCHAR2(255) NOT NULL,
    supplier_id VARCHAR2(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,  -- Field to store soft delete information
    CONSTRAINT fk_supplier FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);
