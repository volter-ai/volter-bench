import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardHeader as ShadcnCardHeader,
  CardContent as ShadcnCardContent,
  CardFooter as ShadcnCardFooter,
  CardTitle as ShadcnCardTitle,
  CardDescription as ShadcnCardDescription,
} from "@/components/ui/card"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <ShadcnCard ref={ref} className={cn("rounded-xl border bg-card text-card-foreground shadow", className)} {...props} />
  )
)

let CardHeader = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <ShadcnCardHeader ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
)

let CardTitle = React.forwardRef<HTMLParagraphElement, CardProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, uid, ...props }, ref) => (
    <ShadcnCardTitle ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
  )
)

let CardDescription = React.forwardRef<HTMLParagraphElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <ShadcnCardDescription ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
  )
)

let CardContent = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <ShadcnCardContent ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)

let CardFooter = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, uid, ...props }, ref) => (
    <ShadcnCardFooter ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
  )
)

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
CardDescription.displayName = "CardDescription"
CardContent.displayName = "CardContent"
CardFooter.displayName = "CardFooter"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardDescription = withClickable(CardDescription)
CardContent = withClickable(CardContent)
CardFooter = withClickable(CardFooter)

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent
}
