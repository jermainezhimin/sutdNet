####################
# Initializing Graph
####################

#Basic graph
nodes <- read.csv("/Users/jermainezhimin/Desktop/Socio Project/nodeF.csv", header=T, as.is=T)
links <- read.csv("/Users/jermainezhimin/Desktop/Socio Project/edgeF.csv", header=T, as.is=T)
library(igraph)
net <- graph.data.frame(links, nodes, directed=F)

##################
# Graph properties
##################

#Vertices
V(net)$label.family <- "Helvetica"
V(net)$label <- NA
V(net)$label.color <- "black"
V(net)$label.cex <- 0.2
V(net)$frame.color <- NA
V(net)$size <- 7.5

#Edges
E(net)$width <- 0.5

#Layout
l <- layout.kamada.kawai(net)

##################
# Graph Sex Plot
##################
V(net)$color <- ifelse(V(net)$name.Sex == 'M',rgb(0.3,0.4,0.7,alpha=0.5),rgb(0.7,0.4,0.3,alpha=0.5))
plot(net, layout = l)
legCol = c(rgb(0.3,0.4,0.7,alpha=0.5),rgb(0.7,0.4,0.3,alpha=0.5))
legend(x=-1.5, y=1.1, c(' Male',' Female'), pch=21, bty="n", 
       pt.bg=legCol, pt.cex=2, pt.lwd = 0, 
       cex=.8, y.intersp =2, text.col=rgb(0.5,0.5,0.5), ncol=1)

##################
# Graph Pillar Plot
##################
V(net)$color <- ifelse(V(net)$name.Pillar == 'EPD',rgb(0.7,0.4,0.3,alpha=0.5),
                ifelse(V(net)$name.Pillar == 'ISTD',rgb(0.4,0.7,0.3,alpha=0.5),
                ifelse(V(net)$name.Pillar == 'ESD',rgb(0.3,0.4,0.7,alpha=0.5), rgb(0.4,0.4,0.4,alpha=0.5 ))))
plot(net, layout = l)
legCol = c(rgb(0.7,0.4,0.3,alpha=0.5),rgb(0.4,0.7,0.3,alpha=0.5),rgb(0.3,0.4,0.7,alpha=0.5),rgb(0.4,0.4,0.4,alpha=0.5 ))
legend(x=-1.5, y=1.1, c(' EPD',' ISTD',' ESD',' ASD'), pch=21, bty="n",
       pt.bg=legCol, pt.cex=2, pt.lwd = 0,
       cex=.8, y.intersp =2, text.col=rgb(0.5,0.5,0.5), ncol=1)

##################
# Graph Class Plot
##################
V(net)$color <- ifelse(V(net)$name.Class == 'F01',rgb(0.02,0.68,0.83,alpha=0.5),
                ifelse(V(net)$name.Class == 'F02',rgb(0.03,0.40,0.53,alpha=0.5),
                ifelse(V(net)$name.Class == 'F03',rgb(0.94,0.78,0.03,alpha=0.5),
                ifelse(V(net)$name.Class == 'F04',rgb(0.86,0.10,0.10,alpha=0.5),
                ifelse(V(net)$name.Class == 'F05',rgb(0.29,0.48,0.34,alpha=0.5), rgb(0.96,0.58,0.75,alpha=0.5 ))))))
plot(net, layout = l)
legCol = c(rgb(0.02,0.68,0.83,alpha=0.5),rgb(0.03,0.40,0.53,alpha=0.5),rgb(0.94,0.78,0.03,alpha=0.5),
           rgb(0.86,0.10,0.10,alpha=0.5),rgb(0.29,0.48,0.34,alpha=0.5),rgb(0.96,0.58,0.75,alpha=0.5) )
legend(x=-1.5, y=1.1, c(' F01',' F02',' F03',' F04',' F05',' F06'), pch=21, bty="n",
       pt.bg=legCol, pt.cex=2, pt.lwd = 0,
       cex=.8, y.intersp =2, text.col=rgb(0.5,0.5,0.5), ncol=1)

##################
# Degree Plot
##################

deg <- degree(net, mode="all")
V(net)$label <- paste( nodes$Names , deg , sep="\n")

# If we know the top 3 people(Freshmore)
# V(net)$label <- ifelse(V(net)$name == 'Tiang Hui Hui',paste( nodes$Names , deg , sep="\n"),
#                 ifelse(V(net)$name == 'Chok Xin Lin',paste( nodes$Names , deg , sep="\n"),
#                 ifelse(V(net)$name == 'Ong Yi Qing',paste( nodes$Names , deg , sep="\n"), NA )))
# 
# V(net)$color <- ifelse(V(net)$name == 'Tiang Hui Hui',rgb(0.02,0.68,0.83,alpha=0.5),
#                 ifelse(V(net)$name == 'Chok Xin Lin',rgb(0.03,0.40,0.53,alpha=0.5),
#                 ifelse(V(net)$name == 'Ong Yi Qing',rgb(0.94,0.78,0.03,alpha=0.5), rgb(0.7,0.7,0.7,alpha=0.2 ))))
#
# If we know the top 3 people(Pillar)
# V(net)$label <- ifelse(V(net)$name == 'Chok Xin Lin',paste( nodes$Names , deg , sep="\n"),
#                 ifelse(V(net)$name == 'Poh Wan Han',paste( nodes$Names , deg , sep="\n"), NA ))
# 
# V(net)$color <- ifelse(V(net)$name == 'Chok Xin Lin',rgb(0.03,0.40,0.53,alpha=0.5),
#                 ifelse(V(net)$name == 'Poh Wan Han',rgb(0.94,0.78,0.03,alpha=0.5), rgb(0.7,0.7,0.7,alpha=0.2 )))

V(net)$size <- deg*2
plot(net, layout = l)

##################
# Broker Plot
##################

bet <- betweenness(net, directed=F, weights=NA)
V(net)$label <- ifelse(bet/max(bet)>0.4 , paste( nodes$Names , bet/max(bet) , sep="\n"), NA)
V(net)$size <- 3
V(net)$color <- ifelse(bet/max(bet)>0.4  , rgb(bet/max(bet), 0, 0,alpha=0.5), rgb(0, 0, 0,alpha=0.5))
plot(net, layout = l)
legend(x=-1.5, y=1.1, c(' Broker'), pch=21, bty="n",
       pt.bg=(rgb(0.5, 0, 0,alpha=0.5)), pt.cex=2, pt.lwd = 0,
       cex=.8, y.intersp =2, text.col=rgb(0.5,0.5,0.5), ncol=1)

##################
# Community Plot
##################

ceb <- cluster_edge_betweenness(net)
V(net)$label <- nodes$Names
plot(ceb, net, layout=l)

##################
# Max Dist Plot
##################

diam <- get_diameter(net, directed=F)
vcol <- rep(rgb(0.1,0.1,0.1,alpha=0.5), vcount(net))
vcol[diam] <- "gold"
ecol <- rep("gray80", ecount(net))
ecol[E(net, path=diam)] <- "orange" 
# E(net, path=diam) finds edges along a path, here 'diam'
plot(net, vertex.color=vcol, edge.color=ecol, edge.arrow.mode=0, layout=l)

######################
# Degree Distribution
######################

deg.dist <- degree_distribution(net, cumulative=T, mode="all")
plot( x=0:max(deg), y=1-deg.dist, pch=19, cex=1.2, col="orange", 
      xlab="Degree", ylab="Cumulative Frequency")
