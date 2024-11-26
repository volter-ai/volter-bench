import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as BaseCard, CardContent as BaseCardContent, CardHeader as BaseCardHeader, CardTitle as BaseCardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCard ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCardTitle ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, CardProps>(
  ({ uid, ...props }, ref) => <BaseCardContent ref={ref} {...props} />
)

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
CardContent.displayName = "CardContent"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
          <div className="text-sm">
            HP: {hp}/{maxHp}
          </div>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard, Card, CardHeader, CardTitle, CardContent }
