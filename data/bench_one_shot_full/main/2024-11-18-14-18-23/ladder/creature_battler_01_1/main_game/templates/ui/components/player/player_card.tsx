import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardHeader as ShadcnCardHeader,
  CardContent as ShadcnCardContent,
  CardFooter as ShadcnCardFooter,
  CardTitle as ShadcnCardTitle,
} from "@/components/ui/card"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardContent.displayName = "CardContent"
CardTitle.displayName = "CardTitle"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardContent = withClickable(CardContent)
CardTitle = withClickable(CardTitle)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
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
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
