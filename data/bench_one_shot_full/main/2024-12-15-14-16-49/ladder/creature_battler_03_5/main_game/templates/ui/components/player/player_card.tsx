import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface PlayerCardProps extends BaseCardProps {
  name: string
  imageUrl: string
}

let CustomCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

CustomCard.displayName = "CustomCard"
CustomCardHeader.displayName = "CustomCardHeader"
CustomCardTitle.displayName = "CustomCardTitle"
CustomCardContent.displayName = "CustomCardContent"

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardTitle = withClickable(CustomCardTitle)
CustomCardContent = withClickable(CustomCardContent)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <CustomCard ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
      <CustomCardHeader uid={`${uid}-header`}>
        <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
      </CustomCardHeader>
      <CustomCardContent uid={`${uid}-content`}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </CustomCardContent>
    </CustomCard>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
