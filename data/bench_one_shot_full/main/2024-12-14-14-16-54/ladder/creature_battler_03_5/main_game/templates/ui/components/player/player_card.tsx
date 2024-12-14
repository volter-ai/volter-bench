import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

interface CardComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CustomCard = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ uid, ...props }, ref) => <Card {...props} ref={ref} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ uid, ...props }, ref) => <CardHeader {...props} ref={ref} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, CardComponentProps>(
  ({ uid, ...props }, ref) => <CardContent {...props} ref={ref} />
)

CustomCard.displayName = "CustomCard"
CustomCardHeader.displayName = "CustomCardHeader"
CustomCardContent.displayName = "CustomCardContent"

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardContent = withClickable(CustomCardContent)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <CustomCard uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
      <CustomCardHeader uid={`${uid}-header`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </CustomCardHeader>
      <CustomCardContent uid={`${uid}-content`}>
        <h3 className="text-lg font-bold text-center">{name}</h3>
      </CustomCardContent>
    </CustomCard>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
