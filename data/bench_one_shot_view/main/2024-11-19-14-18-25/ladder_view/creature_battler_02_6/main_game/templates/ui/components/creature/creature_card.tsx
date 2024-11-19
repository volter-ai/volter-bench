import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

// Base components with uid
let Card = React.forwardRef<
  HTMLDivElement, 
  React.ComponentPropsWithRef<typeof ShadcnCard> & { uid: string }
>(({ uid, ...props }, ref) => (
  <ShadcnCard ref={ref} {...props} />
))

let CardContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof ShadcnCardContent> & { uid: string }
>(({ uid, ...props }, ref) => (
  <ShadcnCardContent ref={ref} {...props} />
))

let CardHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof ShadcnCardHeader> & { uid: string }
>(({ uid, ...props }, ref) => (
  <ShadcnCardHeader ref={ref} {...props} />
))

let CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.ComponentPropsWithRef<typeof ShadcnCardTitle> & { uid: string }
>(({ uid, ...props }, ref) => (
  <ShadcnCardTitle ref={ref} {...props} />
))

// Apply withClickable
Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

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
          <div className="text-sm text-muted-foreground">
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

export { CreatureCard }
