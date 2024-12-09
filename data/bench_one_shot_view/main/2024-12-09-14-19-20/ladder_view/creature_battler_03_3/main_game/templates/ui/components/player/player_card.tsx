import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as BaseCard, CardContent as BaseCardContent, CardHeader as BaseCardHeader, CardTitle as BaseCardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCard {...props} ref={ref} />
)

let CardContent = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCardContent {...props} ref={ref} />
)

let CardHeader = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCardHeader {...props} ref={ref} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, CardProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ uid, ...props }, ref) => <BaseCardTitle {...props} ref={ref} />
)

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={uid}>
          <CardTitle uid={uid}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={uid}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-cover rounded-md"
          />
        </CardContent>
      </Card>
    )
  }
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
