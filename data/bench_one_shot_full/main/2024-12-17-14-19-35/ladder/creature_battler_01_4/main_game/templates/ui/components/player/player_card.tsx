import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardContent as ShadcnCardContent,
  CardHeader as ShadcnCardHeader,
  CardTitle as ShadcnCardTitle,
} from "@/components/ui/card"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCard ref={ref} {...props} />
))

let CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardHeader ref={ref} {...props} />
))

let CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardTitle ref={ref} {...props} />
))

let CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardContent ref={ref} {...props} />
))

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card uid={uid} className={cn("w-[350px]", className)} {...props}>
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
