import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
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
      <Card ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={uid}>
          <CardTitle uid={uid}>{name}</CardTitle>
          <div className="text-sm">
            HP: {hp}/{maxHp}
          </div>
        </CardHeader>
        <CardContent uid={uid}>
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

export { Card, CardHeader, CardTitle, CardContent, CreatureCard }
