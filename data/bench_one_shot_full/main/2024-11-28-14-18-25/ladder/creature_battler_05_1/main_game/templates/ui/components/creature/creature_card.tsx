import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"

interface BaseProps {
  uid: string
}

let Progress = React.forwardRef<
  React.ElementRef<typeof ShadcnProgress>,
  React.ComponentPropsWithoutRef<typeof ShadcnProgress> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnProgress {...props} ref={ref} />
))

let Card = React.forwardRef<
  React.ElementRef<typeof ShadcnCard>,
  React.ComponentPropsWithoutRef<typeof ShadcnCard> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCard {...props} ref={ref} />
))

let CardContent = React.forwardRef<
  React.ElementRef<typeof ShadcnCardContent>,
  React.ComponentPropsWithoutRef<typeof ShadcnCardContent> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardContent {...props} ref={ref} />
))

let CardHeader = React.forwardRef<
  React.ElementRef<typeof ShadcnCardHeader>,
  React.ComponentPropsWithoutRef<typeof ShadcnCardHeader> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardHeader {...props} ref={ref} />
))

let CardTitle = React.forwardRef<
  React.ElementRef<typeof ShadcnCardTitle>,
  React.ComponentPropsWithoutRef<typeof ShadcnCardTitle> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardTitle {...props} ref={ref} />
))

Progress.displayName = "Progress"
Card.displayName = "Card"
CardContent.displayName = "CardContent"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"

Progress = withClickable(Progress)
Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img
              src={image}
              alt={name}
              className="h-[200px] w-full object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{`${currentHp}/${maxHp}`}</span>
              </div>
              <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
