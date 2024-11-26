import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardContent as ShadcnCardContent,
  CardFooter as ShadcnCardFooter,
  CardHeader as ShadcnCardHeader,
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

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
)

let CardFooter = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <ShadcnCardFooter ref={ref} {...props} />
)

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
CardContent.displayName = "CardContent"
CardFooter.displayName = "CardFooter"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)
CardFooter = withClickable(CardFooter)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain"
          />
        </CardContent>
        <CardFooter uid={`${uid}-footer`}>
          <div className="w-full">
            <div className="flex justify-between mb-1">
              <span>HP</span>
              <span>{`${currentHp}/${maxHp}`}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-green-600 h-2.5 rounded-full"
                style={{ width: `${(currentHp / maxHp) * 100}%` }}
              />
            </div>
          </div>
        </CardFooter>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
