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

let Card = React.forwardRef<
  HTMLDivElement, 
  React.ComponentPropsWithRef<typeof ShadcnCard> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCard ref={ref} {...props} />
))

let CardHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof ShadcnCardHeader> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardHeader ref={ref} {...props} />
))

let CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.ComponentPropsWithRef<typeof ShadcnCardTitle> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardTitle ref={ref} {...props} />
))

let CardContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof ShadcnCardContent> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardContent ref={ref} {...props} />
))

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
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-contain"
            />
            <div className="flex justify-between">
              <span>HP:</span>
              <span>{hp}/{maxHp}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
CardContent.displayName = "CardContent"
CreatureCard.displayName = "CreatureCard"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)
CreatureCard = withClickable(CreatureCard)

export { Card, CardHeader, CardTitle, CardContent, CreatureCard }
