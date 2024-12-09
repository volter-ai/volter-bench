import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
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
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="aspect-square w-full relative mb-4">
            <img
              src={imageUrl}
              alt={name}
              className="rounded-lg object-cover w-full h-full"
            />
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">HP</span>
            <span className="text-sm font-medium">{`${hp}/${maxHp}`}</span>
          </div>
          <div className="w-full h-2 bg-secondary rounded-full mt-2">
            <div
              className="h-full bg-primary rounded-full"
              style={{ width: `${(hp / maxHp) * 100}%` }}
            />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
