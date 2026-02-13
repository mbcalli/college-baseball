"""Database models for bronze and silver layers."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Float, Integer, String, Text, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


# Bronze Layer Models - Raw Data


class BronzeAdvBatting(Base):
    """Bronze layer: Advanced batting statistics."""

    __tablename__ = "bronze_adv_batting"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Statistics
    pa: Mapped[Optional[int]] = mapped_column(Integer)
    bb_rate: Mapped[Optional[float]] = mapped_column(Float)
    k_rate: Mapped[Optional[float]] = mapped_column(Float)
    bb_per_k: Mapped[Optional[float]] = mapped_column(Float)
    avg: Mapped[Optional[float]] = mapped_column(Float)
    obp: Mapped[Optional[float]] = mapped_column(Float)
    slg: Mapped[Optional[float]] = mapped_column(Float)
    ops: Mapped[Optional[float]] = mapped_column(Float)
    iso: Mapped[Optional[float]] = mapped_column(Float)
    spd: Mapped[Optional[float]] = mapped_column(Float)
    babip: Mapped[Optional[float]] = mapped_column(Float)
    wsb: Mapped[Optional[float]] = mapped_column(Float)
    wrc: Mapped[Optional[float]] = mapped_column(Float)
    wraa: Mapped[Optional[float]] = mapped_column(Float)
    woba: Mapped[Optional[float]] = mapped_column(Float)
    wrc_plus: Mapped[Optional[float]] = mapped_column(Float)
    
    alt_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_bronze_adv_batting_team", "team"),
        Index("idx_bronze_adv_batting_name", "name"),
    )


class BronzeStdBatting(Base):
    """Bronze layer: Standard batting statistics."""

    __tablename__ = "bronze_std_batting"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Statistics
    g: Mapped[Optional[int]] = mapped_column(Integer)
    ab: Mapped[Optional[int]] = mapped_column(Integer)
    pa: Mapped[Optional[int]] = mapped_column(Integer)
    h: Mapped[Optional[int]] = mapped_column(Integer)
    single: Mapped[Optional[int]] = mapped_column(Integer)
    double: Mapped[Optional[int]] = mapped_column(Integer)
    triple: Mapped[Optional[int]] = mapped_column(Integer)
    hr: Mapped[Optional[int]] = mapped_column(Integer)
    r: Mapped[Optional[int]] = mapped_column(Integer)
    rbi: Mapped[Optional[int]] = mapped_column(Integer)
    bb: Mapped[Optional[int]] = mapped_column(Integer)
    ibb: Mapped[Optional[int]] = mapped_column(Integer)
    so: Mapped[Optional[int]] = mapped_column(Integer)
    hbp: Mapped[Optional[int]] = mapped_column(Integer)
    sf: Mapped[Optional[int]] = mapped_column(Integer)
    sh: Mapped[Optional[int]] = mapped_column(Integer)
    gdp: Mapped[Optional[int]] = mapped_column(Integer)
    sb: Mapped[Optional[int]] = mapped_column(Integer)
    cs: Mapped[Optional[int]] = mapped_column(Integer)
    avg: Mapped[Optional[float]] = mapped_column(Float)
    
    alt_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_bronze_std_batting_team", "team"),
        Index("idx_bronze_std_batting_name", "name"),
    )


class BronzeAdvPitching(Base):
    """Bronze layer: Advanced pitching statistics."""

    __tablename__ = "bronze_adv_pitching"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Statistics
    w: Mapped[Optional[int]] = mapped_column(Integer)
    l: Mapped[Optional[int]] = mapped_column(Integer)
    sv: Mapped[Optional[int]] = mapped_column(Integer)
    g: Mapped[Optional[int]] = mapped_column(Integer)
    gs: Mapped[Optional[int]] = mapped_column(Integer)
    ip: Mapped[Optional[float]] = mapped_column(Float)
    k_per_9: Mapped[Optional[float]] = mapped_column(Float)
    bb_per_9: Mapped[Optional[float]] = mapped_column(Float)
    hr_per_9: Mapped[Optional[float]] = mapped_column(Float)
    babip: Mapped[Optional[float]] = mapped_column(Float)
    lob_pct: Mapped[Optional[float]] = mapped_column(Float)
    gb_pct: Mapped[Optional[float]] = mapped_column(Float)
    hr_per_fb: Mapped[Optional[float]] = mapped_column(Float)
    era: Mapped[Optional[float]] = mapped_column(Float)
    fip: Mapped[Optional[float]] = mapped_column(Float)
    xfip: Mapped[Optional[float]] = mapped_column(Float)
    siera: Mapped[Optional[float]] = mapped_column(Float)
    
    alt_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_bronze_adv_pitching_team", "team"),
        Index("idx_bronze_adv_pitching_name", "name"),
    )


class BronzeStdPitching(Base):
    """Bronze layer: Standard pitching statistics."""

    __tablename__ = "bronze_std_pitching"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Statistics
    w: Mapped[Optional[int]] = mapped_column(Integer)
    l: Mapped[Optional[int]] = mapped_column(Integer)
    era: Mapped[Optional[float]] = mapped_column(Float)
    g: Mapped[Optional[int]] = mapped_column(Integer)
    gs: Mapped[Optional[int]] = mapped_column(Integer)
    cg: Mapped[Optional[int]] = mapped_column(Integer)
    sho: Mapped[Optional[int]] = mapped_column(Integer)
    sv: Mapped[Optional[int]] = mapped_column(Integer)
    ip: Mapped[Optional[float]] = mapped_column(Float)
    h: Mapped[Optional[int]] = mapped_column(Integer)
    r: Mapped[Optional[int]] = mapped_column(Integer)
    er: Mapped[Optional[int]] = mapped_column(Integer)
    hr: Mapped[Optional[int]] = mapped_column(Integer)
    bb: Mapped[Optional[int]] = mapped_column(Integer)
    ibb: Mapped[Optional[int]] = mapped_column(Integer)
    hbp: Mapped[Optional[int]] = mapped_column(Integer)
    wp: Mapped[Optional[int]] = mapped_column(Integer)
    bk: Mapped[Optional[int]] = mapped_column(Integer)
    so: Mapped[Optional[int]] = mapped_column(Integer)
    
    alt_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_bronze_std_pitching_team", "team"),
        Index("idx_bronze_std_pitching_name", "name"),
    )


# Silver Layer Models - Percentile Rankings


class SilverAdvBatting(Base):
    """Silver layer: Advanced batting percentiles."""

    __tablename__ = "silver_adv_batting"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Percentiles (0-100)
    pa_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    bb_rate_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    k_rate_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    bb_per_k_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    avg_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    obp_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    slg_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    ops_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    iso_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    spd_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    babip_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    wsb_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    wrc_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    wraa_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    woba_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    wrc_plus_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_silver_adv_batting_team", "team"),
    )


class SilverStdBatting(Base):
    """Silver layer: Standard batting percentiles."""

    __tablename__ = "silver_std_batting"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Percentiles
    g_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    ab_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    pa_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    h_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    single_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    double_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    triple_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    hr_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    r_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    rbi_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    bb_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    ibb_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    so_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    hbp_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    sf_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    sh_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    gdp_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    sb_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    cs_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    avg_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_silver_std_batting_team", "team"),
    )


class SilverAdvPitching(Base):
    """Silver layer: Advanced pitching percentiles."""

    __tablename__ = "silver_adv_pitching"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Percentiles
    w_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    l_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    sv_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    g_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    gs_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    ip_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    k_per_9_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    bb_per_9_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    hr_per_9_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    babip_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    lob_pct_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    gb_pct_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    hr_per_fb_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    era_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    fip_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    xfip_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    siera_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_silver_adv_pitching_team", "team"),
    )


class SilverStdPitching(Base):
    """Silver layer: Standard pitching percentiles."""

    __tablename__ = "silver_std_pitching"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    data_date: Mapped[datetime] = mapped_column(DateTime, primary_key=True, default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    team: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Percentiles
    w_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    l_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    era_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    g_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    gs_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    cg_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    sho_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    sv_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    ip_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    h_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    r_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    er_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    hr_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    bb_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    ibb_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    hbp_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    wp_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    bk_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    so_percentile: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_silver_std_pitching_team", "team"),
    )
