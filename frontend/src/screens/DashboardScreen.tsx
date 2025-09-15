import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Dimensions,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  FAB,
  Chip,
  ProgressBar,
  Text,
} from 'react-native-paper';
import { useSelector, useDispatch } from 'react-redux';
import { LineChart, PieChart } from 'react-native-chart-kit';
import { useTranslation } from 'react-i18next';

import { RootState } from '../store/store';
import { fetchDashboardData } from '../store/slices/dashboardSlice';
import { theme } from '../theme/theme';

const { width } = Dimensions.get('window');

const DashboardScreen: React.FC = () => {
  const { t } = useTranslation();
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { dashboardData, isLoading } = useSelector((state: RootState) => state.dashboard);
  const { language } = useSelector((state: RootState) => state.app);
  
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    dispatch(fetchDashboardData());
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    const name = user?.full_name?.split(' ')[0] || 'दोस्त';
    
    if (language === 'hindi') {
      if (hour < 12) return `सुप्रभात, ${name}!`;
      else if (hour < 17) return `नमस्कार, ${name}!`;
      else return `शुभ संध्या, ${name}!`;
    } else {
      if (hour < 12) return `Good Morning, ${name}!`;
      else if (hour < 17) return `Good Afternoon, ${name}!`;
      else return `Good Evening, ${name}!`;
    }
  };

  const salesData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: dashboardData?.weeklyStats?.sales || [0, 0, 0, 0, 0, 0, 0],
        color: (opacity = 1) => `rgba(76, 175, 80, ${opacity})`,
        strokeWidth: 2,
      },
    ],
  };

  const categoryData = dashboardData?.topCategories?.map((category, index) => ({
    name: category.name,
    population: category.sales,
    color: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'][index % 5],
    legendFontColor: '#7F7F7F',
    legendFontSize: 12,
  })) || [];

  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Greeting Card */}
        <Card style={styles.greetingCard}>
          <Card.Content>
            <Title style={styles.greeting}>{getGreeting()}</Title>
            <Paragraph style={styles.businessName}>
              {user?.business_name || 'आपका व्यापार'}
            </Paragraph>
            <View style={styles.statusChips}>
              <Chip
                icon="check-circle"
                style={[styles.chip, styles.activeChip]}
                textStyle={styles.chipText}
              >
                {t('dashboard.active')}
              </Chip>
              <Chip
                icon="trending-up"
                style={[styles.chip, styles.growthChip]}
                textStyle={styles.chipText}
              >
                +12% {t('dashboard.growth')}
              </Chip>
            </View>
          </Card.Content>
        </Card>

        {/* Quick Stats */}
        <View style={styles.statsContainer}>
          <Card style={styles.statCard}>
            <Card.Content style={styles.statContent}>
              <Text style={styles.statNumber}>
                ₹{dashboardData?.todaySales?.toLocaleString('en-IN') || '0'}
              </Text>
              <Text style={styles.statLabel}>{t('dashboard.todaySales')}</Text>
            </Card.Content>
          </Card>
          
          <Card style={styles.statCard}>
            <Card.Content style={styles.statContent}>
              <Text style={styles.statNumber}>
                {dashboardData?.totalOrders || 0}
              </Text>
              <Text style={styles.statLabel}>{t('dashboard.orders')}</Text>
            </Card.Content>
          </Card>
          
          <Card style={styles.statCard}>
            <Card.Content style={styles.statContent}>
              <Text style={styles.statNumber}>
                {dashboardData?.totalCustomers || 0}
              </Text>
              <Text style={styles.statLabel}>{t('dashboard.customers')}</Text>
            </Card.Content>
          </Card>
        </View>

        {/* Sales Chart */}
        <Card style={styles.chartCard}>
          <Card.Content>
            <Title>{t('dashboard.weeklySales')}</Title>
            <LineChart
              data={salesData}
              width={width - 60}
              height={220}
              chartConfig={{
                backgroundColor: '#ffffff',
                backgroundGradientFrom: '#ffffff',
                backgroundGradientTo: '#ffffff',
                decimalPlaces: 0,
                color: (opacity = 1) => `rgba(76, 175, 80, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                style: {
                  borderRadius: 16,
                },
                propsForDots: {
                  r: '6',
                  strokeWidth: '2',
                  stroke: '#4CAF50',
                },
              }}
              bezier
              style={styles.chart}
            />
          </Card.Content>
        </Card>

        {/* Top Categories */}
        {categoryData.length > 0 && (
          <Card style={styles.chartCard}>
            <Card.Content>
              <Title>{t('dashboard.topCategories')}</Title>
              <PieChart
                data={categoryData}
                width={width - 60}
                height={220}
                chartConfig={{
                  color: (opacity = 1) => `rgba(76, 175, 80, ${opacity})`,
                }}
                accessor="population"
                backgroundColor="transparent"
                paddingLeft="15"
                absolute
              />
            </Card.Content>
          </Card>
        )}

        {/* Quick Actions */}
        <Card style={styles.actionsCard}>
          <Card.Content>
            <Title>{t('dashboard.quickActions')}</Title>
            <View style={styles.actionsContainer}>
              <Button
                mode="contained"
                icon="plus"
                style={styles.actionButton}
                onPress={() => {/* Navigate to add inventory */}}
              >
                {t('dashboard.addProduct')}
              </Button>
              <Button
                mode="outlined"
                icon="account-plus"
                style={styles.actionButton}
                onPress={() => {/* Navigate to add customer */}}
              >
                {t('dashboard.addCustomer')}
              </Button>
              <Button
                mode="contained"
                icon="cash-register"
                style={[styles.actionButton, styles.saleButton]}
                onPress={() => {/* Navigate to new sale */}}
              >
                {t('dashboard.newSale')}
              </Button>
            </View>
          </Card.Content>
        </Card>

        {/* Recent Activity */}
        <Card style={styles.activityCard}>
          <Card.Content>
            <Title>{t('dashboard.recentActivity')}</Title>
            {dashboardData?.recentActivities?.map((activity, index) => (
              <View key={index} style={styles.activityItem}>
                <Text style={styles.activityText}>{activity.description}</Text>
                <Text style={styles.activityTime}>{activity.time}</Text>
              </View>
            ))}
          </Card.Content>
        </Card>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
    padding: 16,
  },
  greetingCard: {
    marginBottom: 16,
    borderRadius: 12,
    elevation: 4,
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
  businessName: {
    fontSize: 16,
    color: theme.colors.onSurfaceVariant,
    marginBottom: 12,
  },
  statusChips: {
    flexDirection: 'row',
    gap: 8,
  },
  chip: {
    marginRight: 8,
  },
  activeChip: {
    backgroundColor: '#E8F5E8',
  },
  growthChip: {
    backgroundColor: '#E3F2FD',
  },
  chipText: {
    fontSize: 12,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
    gap: 8,
  },
  statCard: {
    flex: 1,
    borderRadius: 12,
    elevation: 2,
  },
  statContent: {
    alignItems: 'center',
    paddingVertical: 8,
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
  statLabel: {
    fontSize: 12,
    color: theme.colors.onSurfaceVariant,
    marginTop: 4,
  },
  chartCard: {
    marginBottom: 16,
    borderRadius: 12,
    elevation: 4,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  actionsCard: {
    marginBottom: 16,
    borderRadius: 12,
    elevation: 4,
  },
  actionsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginTop: 8,
  },
  actionButton: {
    flex: 1,
    minWidth: '30%',
  },
  saleButton: {
    backgroundColor: theme.colors.secondary,
  },
  activityCard: {
    marginBottom: 100, // Space for FAB
    borderRadius: 12,
    elevation: 4,
  },
  activityItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  activityText: {
    flex: 1,
    fontSize: 14,
  },
  activityTime: {
    fontSize: 12,
    color: theme.colors.onSurfaceVariant,
  },
});

export default DashboardScreen;